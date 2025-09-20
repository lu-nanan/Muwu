import json
import re
import sys

from rest_framework.decorators import api_view
from rest_framework.response import Response

from MarkFlowImpl.models import BaseVocabulary, User, UserWords
from MarkFlowImpl.utils.get_word_analysis import  batch_get_word_analysis2
from MarkFlowImpl.utils.import_words_to_db import import_words_to_db
from MarkFlowImpl.utils.spell_checker import validate_words


def extract_words(words):
    # 如果是单个单词，转为数组
    #if isinstance(words, str):
        #words = [words]
    cleaned_words = []
    excluded_words = []


    for word in words:
        stripped_word = word.strip().lower()

        # 跳过空字符串
        if not stripped_word:
            print(f"跳过空字符串: '{word}'")
            continue

        # 检查是否包含数字
        if re.search(r'\d', stripped_word):
            excluded_words.append(stripped_word)
            continue

        cleaned_words.append(stripped_word)

    if excluded_words:
        print(f"  排除列表: {excluded_words}")

    return cleaned_words
@api_view(['POST'])
def word_search(request):
    print("\n=== 开始处理单词查询请求 ===")
    try:
        # 1. 从请求中提取单词列表
        print("[步骤1] 正在解析请求数据...")
        words_data = request.data.get('words', [])
        if not words_data:
            error_msg = "请求数据中缺少 'words' 字段"
            print(f"[错误] {error_msg}")
            return Response({'success': False, 'error': error_msg})

        print(f"[信息] 成功获取 {len(words_data)} 个单词")

        # 2. 提取并清洗单词
        print("[步骤2] 正在清洗和规范化单词...")
        words = extract_words(words_data)
        words , misspelled_dict = validate_words(words)
        for word in words:
            print(f"[<UNK>3] {word}")


        print(f"[信息] 清洗后有效单词: {len(words)} 个")

        # 3. 在基础词库中批量查询单词
        print("[步骤3] 正在查询数据库...")
        word_queryset = BaseVocabulary.objects.filter(word__in=words)
        found_words_map = {obj.word: obj for obj in word_queryset}

        print(f"[信息] 数据库中找到 {len(found_words_map)} 个单词")

        # 4. 构建结果集
        print("[步骤4] 正在构建响应数据...")
        result = []
        not_found_words = []

        for word in words:
            #normalized_word = word.strip().lower()
            if word in found_words_map:
                word_obj = found_words_map[word]
                result.append({
                    'word': word_obj.word,
                    'soundmark': word_obj.pronunciation or '',
                    'explain': word_obj.definition or '',
                    'sentence': word_obj.example_sentence or '',
                    'about': word_obj.synonyms or '',
                    'found_in_db': True
                })
            else:
                not_found_words.append(word)
        print(f"[信息] 构建完成: 数据库搜索到{len(result)} 个单词结果")
        if not_found_words:
            print(f"[信息] 数据库未找到的单词: {', '.join(not_found_words)}")
            # 获取单词分析数据
            not_found_words_analysis = batch_get_word_analysis2(
                not_found_words,
                ""
            )
            import_words_to_db(not_found_words_analysis)
            word_queryset = BaseVocabulary.objects.filter(word__in=not_found_words)
            not_found_words_map = {obj.word: obj for obj in word_queryset}
            for word in not_found_words:
                # normalized_word = word.strip().lower()
                if word in not_found_words_map:
                    word_obj = not_found_words_map[word]
                    result.append({
                        'word': word_obj.word,
                        'soundmark': word_obj.pronunciation or '',
                        'explain': word_obj.definition or '',
                        'sentence': word_obj.example_sentence or '',
                        'about': word_obj.synonyms or '',
                        'found_in_db': True
                    })

            # 打印分析结果
            for word in not_found_words:
                word_entry = not_found_words_analysis.get(word)
                print(json.dumps(word_entry, indent=2, ensure_ascii=False))
            # 导入数据库 - 现在传入字典格式
        for word,suggestions in misspelled_dict.items():
            if suggestions == "无有效单词":tip=suggestions
            else: tip = "未查找到相关单词，请核对你的拼写，可能想查找的单词："+suggestions
            result.append({
                'word': word,
                'soundmark': '',
                'explain': tip,
                'sentence': '',
                'about': '',
                'found_in_db': False
            })
        # 5. 返回成功响应
        print("[步骤5] 返回响应数据")
        print("=== 单词查询处理完成 ===\n")

        return Response({'success': True, 'words': result})

    except ValueError as ve:
        print(f"[错误] 业务逻辑错误: {str(ve)}")

        return Response({'success': False, 'error': str(ve)})

    except Exception as e:
        print(f"[严重错误] 内部错误: {str(e)}")
        print(f"[错误详情] {sys.exc_info()}")  # 打印完整错误堆栈
        return Response({'success': False, 'error': '服务器内部错误，请稍后重试'})

def process_words_request1(words_data, user_id=None):
    """处理单词请求的公共函数"""
    print("[步骤1] 正在解析请求数据...")
    if not words_data:
        error_msg = "请求数据中缺少 'words' 字段"
        print(f"[错误] {error_msg}")
        return {'success': False, 'error': error_msg}

    print(f"[信息] 成功获取 {len(words_data)} 个单词")
    if user_id:
        print(f"[信息] 用户ID: {user_id}")

    # 提取并清洗单词
    print("[步骤2] 正在清洗和规范化单词...")
    words = extract_words(words_data)
    words, misspelled_dict = validate_words(words)

    for word in words:
        print(f"[信息] 处理单词: {word}")

    print(f"[信息] 清洗后有效单词: {len(words)} 个")

    # 在基础词库中批量查询单词
    print("[步骤3] 正在查询数据库...")
    word_queryset = BaseVocabulary.objects.filter(word__in=words)
    found_words_map = {obj.word: obj for obj in word_queryset}

    print(f"[信息] 数据库中找到 {len(found_words_map)} 个单词")

    # 构建结果集
    print("[步骤4] 正在构建响应数据...")
    result = []
    not_found_words = []

    for word in words:
        if word in found_words_map:
            word_obj = found_words_map[word]
            result.append({
                'word': word_obj.word,
                'soundmark': word_obj.pronunciation or '',
                'explain': word_obj.definition or '',
                'sentence': word_obj.example_sentence or '',
                'about': word_obj.synonyms or '',
                'found_in_db': True
            })
        else:
            not_found_words.append(word)

    print(f"[信息] 构建完成: 数据库搜索到{len(result)} 个单词结果")

    # 处理未找到的单词
    if not_found_words:
        print(f"[信息] 数据库未找到的单词: {', '.join(not_found_words)}")
        # 获取单词分析数据
        not_found_words_analysis = batch_get_word_analysis2(
            not_found_words,
            ""
        )
        import_words_to_db(not_found_words_analysis)

        # 重新查询数据库获取新导入的单词
        word_queryset = BaseVocabulary.objects.filter(word__in=not_found_words)
        not_found_words_map = {obj.word: obj for obj in word_queryset}

        for word in not_found_words:
            if word in not_found_words_map:
                word_obj = not_found_words_map[word]
                result.append({
                    'word': word_obj.word,
                    'soundmark': word_obj.pronunciation or '',
                    'explain': word_obj.definition or '',
                    'sentence': word_obj.example_sentence or '',
                    'about': word_obj.synonyms or '',
                    'found_in_db': True
                })

        # 打印分析结果
        for word in not_found_words:
            word_entry = not_found_words_analysis.get(word)
            print(json.dumps(word_entry, indent=2, ensure_ascii=False))

    # 处理拼写错误的单词
    for word, suggestions in misspelled_dict.items():
        if suggestions == "无有效单词":
            tip = suggestions
        else:
            tip = "未查查找相关单词，请核对你的拼写，可能想查找的单词：" + suggestions

        result.append({
            'word': word,
            'soundmark': '',
            'explain': tip,
            'sentence': '',
            'about': '',
            'found_in_db': False
        })

    # 如果需要绑定用户，处理绑定逻辑
    if user_id:
        print("[步骤5] 正在将单词与用户绑定...")
        try:
            user = User.objects.get(id=user_id)

            # 获取所有有效的单词对象
            valid_words = BaseVocabulary.objects.filter(word__in=words)

            # 将每个单词与用户绑定
            for word_obj in valid_words:
                # 检查是否已存在绑定关系
                if not UserWords.objects.filter(user=user, word=word_obj).exists():
                    UserWords.objects.create(
                        user=user,
                        word=word_obj,  # 这里使用单词对象，Django会自动处理ID关联
                        #source='base_vocab'  # 根据您的SOURCE_CHOICES设置适当的来源
                    )
                    print(f"[信息] 已绑定单词: {word_obj.word} (ID: {word_obj.id}) 到用户: {user_id}")
                else:
                    print(f"[信息] 单词 {word_obj.word} (ID: {word_obj.id}) 已绑定到用户，跳过")

        except User.DoesNotExist:
            error_msg = f"用户ID {user_id} 不存在"
            print(f"[错误] {error_msg}")
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f"绑定单词到用户时发生错误: {str(e)}"
            print(f"[错误] {error_msg}")
            return {'success': False, 'error': error_msg}

    return {'success': True, 'words': result}


@api_view(['POST'])
def word_search(request):
    print("\n=== 开始处理单词查询请求 ===")
    try:
        words_data = request.data.get('words', [])
        result = process_words_request1(words_data)

        if not result['success']:
            return Response(result)

        print("=== 单词查询处理完成 ===\n")
        return Response(result)

    except Exception as e:
        print(f"[严重错误] 内部错误: {str(e)}")
        import traceback
        print(f"[错误详情] {traceback.format_exc()}")
        return Response({'success': False, 'error': '服务器内部错误，请稍后重试'})


@api_view(['POST'])
def word_add(request):
    print("\n=== 开始处理单词添加请求 ===")
    try:
        words_data = request.data.get('words', [])
        user_id = request.data.get('user_id')

        if not user_id:
            error_msg = "请求数据中缺少 'user_id' 字段"
            print(f"[错误] {error_msg}")
            return Response({'success': False, 'error': error_msg})

        result = process_words_request1(words_data, user_id)

        if not result['success']:
            return Response(result)

        print("=== 单词添加处理完成 ===\n")
        return Response(result)

    except Exception as e:
        print(f"[严重错误] 内部错误: {str(e)}")
        import traceback
        print(f"[错误详情] {traceback.format_exc()}")
        return Response({'success': False, 'error': '服务器内部错误，请稍后重试'})

