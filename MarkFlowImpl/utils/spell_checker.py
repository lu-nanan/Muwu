from spellchecker import SpellChecker
from typing import List, Dict, Tuple


def validate_words(word_list: List[str]) -> Tuple[List[str], Dict[str, str]]:
    """
    验证小写单词数组，过滤无效单词并提供多个拼写建议
    """
    spell = SpellChecker()
    valid_words = []  # 存储合法单词
    misspelled_dict = {}  # 存储错误单词及其建议修正

    # 打印开始提示
    print(f"\n===== 开始拼写检查，共处理 {len(word_list)} 个单词 =====")

    # 批量识别所有可能的错误单词
    misspelled = spell.unknown(word_list)
    print(f"初步识别到 {len(misspelled)} 个可能的错误单词")

    for word in word_list:
        # 打印当前处理的单词
        print(f"\n处理单词: {word}")

        if word in misspelled:
            # 获取多个修正建议（最多5个）
            candidates = spell.candidates(word)
            print(f"  发现错误拼写，正在生成修正建议...")

            if candidates:
                # 选择最多5个候选词（排除原单词）
                suggestions = [c for c in candidates if c != word][:5]
                print(f"  建议修正: {suggestions}")

                # 如果没有候选词，保留原单词
                if not suggestions:
                    suggestions = "无有效单词"
                    print(f"  未找到有效修正，保留原单词")
            else:
                suggestions = "无有效单词"
                print(f"  未找到任何修正建议，保留原单词")
            if suggestions != "无有效单词":
                # 将建议列表拼接为逗号分隔的字符串
                misspelled_dict[word] = "、".join(suggestions)
                print(f"  错误单词已记录: {word}")
            else: misspelled_dict[word] = suggestions
        else:
            # 合法单词直接加入列表
            valid_words.append(word)
            print(f"  拼写正确，加入有效单词列表")

    # 打印总结信息
    print(f"\n===== 拼写检查完成 =====")
    print(f"  有效单词: {len(valid_words)} 个")
    print(f"  错误单词: {len(misspelled_dict)} 个")
    if misspelled_dict:
        print(f"  错误单词及建议: {misspelled_dict}")

    return valid_words, misspelled_dict