from MarkFlowImpl.models import BaseVocabulary
from typing import Dict
import json
from django.db import transaction  # 添加事务支持


def import_words_to_db(word_data_dict: Dict[str, dict]) -> Dict:
    """
    增强版单词导入函数，支持字典格式输入
    :param word_data_dict: 单词数据字典 {单词: 数据}
    :return: 导入结果统计
    """
    result = {
        'total': len(word_data_dict),
        'success': 0,
        'failed': 0,
        'errors': {}
    }

    # 使用事务确保数据一致性
    with transaction.atomic():
        for word, word_data in word_data_dict.items():
            try:
                # 跳过错误数据
                if 'error' in word_data:
                    result['failed'] += 1
                    result['errors'][word] = word_data['error']
                    continue

                print(f"\n正在处理单词: {word}")

                # 1. 提取基础字段
                pronunciation = word_data.get('us_phonetic', '')

                # 2. 处理释义
                definitions = word_data.get('definition', [])
                definition_text = '\\n'.join(definitions) if isinstance(definitions, list) else definitions

                # 3. 处理例句
                examples = word_data.get('examples', [])
                example_texts = []

                if isinstance(examples, list):
                    for example in examples:
                        if isinstance(example, str):
                            if " || " in example:
                                example_texts.append(example)
                            else:
                                example_texts.append(f"{example} || 暂无中文翻译")
                        elif isinstance(example, dict):
                            en = example.get('en', '')
                            zh = example.get('zh', '')
                            if en:
                                example_texts.append(f"{en}\\n{zh}" if zh else f"{en} || 暂无中文翻译")
                else:
                    print(f"警告: 例句格式不支持 - {examples}")

                example_text = '\\n'.join(example_texts)

                # 4. 处理近义词 - 包含释义
                synonyms = word_data.get('synonyms', [])
                synonym_texts = []

                if isinstance(synonyms, list):
                    for syn in synonyms:
                        if isinstance(syn, dict):
                            word_str = syn.get('word', '')
                            definition = syn.get('definition', '')
                            if word_str:
                                synonym_texts.append(f"{word_str}: {definition}" if definition else word_str)
                        elif isinstance(syn, str):
                            synonym_texts.append(syn)
                else:
                    print(f"警告: 近义词格式不支持 - {synonyms}")

                synonym_text = '\\n'.join(synonym_texts)

                # 5. 处理易混淆词 - 包含释义
                confusing_words = word_data.get('confusing_words', [])
                confusing_texts = []

                if isinstance(confusing_words, list):
                    for cw in confusing_words:
                        if isinstance(cw, dict):
                            word_str = cw.get('word', '')
                            definition = cw.get('definition', '')
                            if word_str:
                                confusing_texts.append(f"{word_str}: {definition}" if definition else word_str)
                        elif isinstance(cw, str):
                            confusing_texts.append(cw)
                else:
                    print(f"警告: 易混淆词格式不支持 - {confusing_words}")

                confusing_words_text = '\\n'.join(confusing_texts)

                # 6. 数据库操作
                BaseVocabulary.objects.update_or_create(
                    word=word,
                    defaults={
                        'pronunciation': pronunciation[:200],  # 限制长度
                        'definition': definition_text[:1000],
                        'example_sentence': example_text[:1000],
                        'synonyms': synonym_text[:500],
                        'confusing_words': confusing_words_text[:500],
                    }
                )
                print(f"✅ 单词 {word} 导入成功")
                result['success'] += 1

            except Exception as e:
                print(f"❌ 处理单词 {word} 时发生致命错误: {str(e)}")
                result['failed'] += 1
                result['errors'][word] = str(e)

    print(f"\n===== 导入结果汇总 =====")
    print(f"总单词数: {result['total']}")
    print(f"成功: {result['success']}")
    print(f"失败: {result['failed']}")
    if result['failed'] > 0:
        print(f"失败详情: {json.dumps(result['errors'], indent=2, ensure_ascii=False)}")

    return result