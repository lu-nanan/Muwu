import dashscope
import json


def get_word_analysis(word: str, api_key: str) -> dict:
    """
    使用通义千问-Turbo-Latest获取单词解析
    :param word: 目标单词
    :param api_key: 千问API密钥
    :return: 结构化单词数据
    """
    dashscope.api_key = api_key

    # 精简指令prompt（适配Turbo模型）
    # 强化指令prompt
    prompt = f"""
        严格解析单词：{word}
        输出JSON格式：
        {{
            "word": "{word}",  # 必须与输入相同
            "us_phonetic": "美式音标",
            "definition": ["词性分组释义"],
            "examples": ["中英例句"],
            "synonyms": [{{"word": "近义词", "definition": "释义"}}],
            "confusing_words": [{{"word": "拼写混淆词", "definition": "释义"}}]
        }}

        硬性要求：
        1. 不要添加任何额外解释
        2. 不要返回相关词或扩展词
        3. 严格保持输出字段名不变

        释义要求：
        - 按词性分组(adj>v>n>adv>其他)
        - 每组词性只一个前缀
        - 同词性释义用分号隔开
        """

    response = dashscope.Generation.call(
        model='qwen-turbo',  # 关键变更：使用Turbo模型
        prompt=prompt,
        result_format='message',
        temperature=0.1,
        seed=123
    )

    if response.status_code == 200:
        return json.loads(response.output['choices'][0]['message']['content'])
    else:
        raise Exception(f"API错误: {response.code} - {response.message}")


# 使用示例
if __name__ == "__main__":
    API_KEY = ""  # 替换为实际API密钥
    word_data = get_word_analysis("word", API_KEY)
    print(json.dumps(word_data, indent=2, ensure_ascii=False))
