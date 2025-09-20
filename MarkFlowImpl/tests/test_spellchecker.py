from spellchecker import SpellChecker


def test_spellchecker():
    # 创建 SpellChecker 实例
    spell = SpellChecker()

    # 1. 检查单词拼写
    words = ["aple", "liked", "speling", "mistake", "banana"]
    misspelled = spell.unknown(words)

    print("\n=== 拼写检查 ===")
    print(f"原始单词: {words}")
    print(f"拼写错误的单词: {list(misspelled)}")

    # 2. 获取纠正建议
    print("\n=== 纠错建议 ===")
    for word in misspelled:
        # 获取最可能的纠正结果
        correction = spell.correction(word)
        # 获取可能的候选词（按可能性排序）
        candidates = spell.candidates(word)
        print(f"错误单词: {word}")
        print(f"推荐纠正: {correction}")
        print(f"候选词: {list(candidates)}")
        print("-" * 30)

    # 3. 计算单词出现频率（词频）
    print("\n=== 词频统计 ===")
    word = "apple"
    frequency = spell.word_frequency[word]
    print(f"单词 '{word}' 的出现频率: {frequency:.6f}")

    # 4. 添加自定义单词（用于专业术语或特定领域词汇）
    print("\n=== 添加自定义单词 ===")
    custom_word = "nlp"  # 自然语言处理 (NLP)，默认词典可能不包含
    print(f"添加前，'{custom_word}' 是否被认为拼写错误: {custom_word in misspelled}")

    # 添加自定义单词
    spell.word_frequency.add(custom_word)
    words_with_custom = words + [custom_word]
    misspelled_after = spell.unknown(words_with_custom)

    print(f"添加后，拼写错误的单词: {list(misspelled_after)}")

    # 5. 处理停用词（忽略常见但无实际意义的词）
    print("\n=== 处理停用词 ===")
    sentence = "the quick brown foox jumped over the lazy dog"
    words_in_sentence = sentence.split()
    misspelled_in_sentence = spell.unknown(words_in_sentence)

    print(f"原始句子: {sentence}")
    print(f"被标记为拼写错误的词: {list(misspelled_in_sentence)}")

    # 假设我们认为 "the" 是停用词，不想检查它
    # 注意：pyspellchecker 没有内置停用词列表，需手动处理
    stopwords = {"the", "a", "an", "over", "in", "on"}
    misspelled_without_stopwords = [word for word in misspelled_in_sentence if word not in stopwords]

    print(f"排除停用词后，拼写错误的词: {misspelled_without_stopwords}")


# 运行测试
if __name__ == "__main__":
    test_spellchecker()