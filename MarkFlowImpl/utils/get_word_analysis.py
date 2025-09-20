from typing import List, Dict

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
            "examples": [{{"en": "英文", "zh": "中文"}}]
            "synonyms": [{{"word": "近义词", "definition": "释义"}}]
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

    #"confusing_words": [{{"word": "拼写混淆词", "definition": "释义"}}]
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


def batch_get_word_analysis(words: List[str], api_key: str) -> Dict[str, dict]:
    """
    批量获取单词解析
    :param words: 单词列表
    :param api_key: 千问API密钥
    :return: 字典格式的单词解析结果 {单词: 解析数据}
    """
    results = {}

    for word in words:
        try:
            # 直接调用单单词处理函数
            results[word] = get_word_analysis(word, api_key)
            print(f"已处理: {word}")
        except Exception as e:
            # 简单错误处理，仅记录错误信息
            print(f"处理 {word} 时出错: {str(e)}")
            results[word] = {"error": str(e)}

    return results


from typing import List, Dict, Union
import dashscope
import json
import time
import random


def batch_get_word_analysis2(words: List[str], api_key: str) -> Dict[str, Union[dict, str]]:
    """
    批量获取单词解析（优化版，减少API调用次数）
    :param words: 单词列表
    :param api_key: 千问API密钥
    :return: 字典格式的单词解析结果 {单词: 解析数据}
    """
    dashscope.api_key = api_key
    results = {}
    batch_size = 10  # 每次处理的单词数量
    max_retries = 3  # 最大重试次数

    # 分批处理单词
    for i in range(0, len(words), batch_size):
        batch = words[i:i + batch_size]

        # 构建批量查询的prompt
        prompt = """
        严格解析以下单词：
        """
        prompt += "\n".join([f"- {word}" for word in batch])
        prompt += """

        为每个单词输出JSON格式：
        {
            "word": "单词",  # 必须与输入相同
            "us_phonetic": "美式音标",
            "definition": ["词性分组释义"],
            "examples": [{"en": "英文", "zh": "中文"}],
            "synonyms": [{"word": "近义词", "definition": "释义"}],
            "confusing_words": [{"word": "拼写混淆词", "definition": "释义"}]
        }

        硬性要求：
        1. 不要添加任何额外解释
        2. 不要返回相关词或扩展词
        3. 严格保持输出字段名不变
        4. 输出必须是有效的JSON数组，包含每个单词的解析结果

        释义要求：
        - 按词性分组(adj>v>n>adv>其他)
        - 每组词性只一个前缀
        - 同词性释义用分号隔开

        输出格式示例：
        [
            {
                "word": "apple",
                "us_phonetic": "/ˈæp.əl/",
                "definition": ["n. 苹果; 苹果树"],
                "examples": [{"en": "I eat an apple every day.", "zh": "我每天吃一个苹果。"}],
                "synonyms": [{"word": "fruit", "definition": "水果"}],
                "confusing_words": [{"word": "appal", "definition": "使惊骇"}]
            },
            {
                "word": "book",
                "us_phonetic": "/bʊk/",
                "definition": ["n. 书; 书籍", "v. 预订; 预约"],
                "examples": [{"en": "I read a book.", "zh": "我读了一本书。"}],
                "synonyms": [{"word": "volume", "definition": "卷册"}],
                "confusing_words": [{"word": "brook", "definition": "小溪"}]
            }
        ]
        """

        for attempt in range(max_retries):
            try:
                response = dashscope.Generation.call(
                    model='qwen-turbo',
                    prompt=prompt,
                    result_format='message',
                    temperature=0.1,
                    seed=123
                )

                if response.status_code == 200:
                    # 解析批量响应
                    content = response.output['choices'][0]['message']['content']
                    batch_results = json.loads(content)

                    # 验证响应结构
                    if not isinstance(batch_results, list):
                        raise ValueError("API返回格式错误: 期望JSON数组")

                    # 处理每个单词的结果
                    for word_data in batch_results:
                        word = word_data.get('word', '').lower()
                        if word in batch:
                            results[word] = word_data
                            print(f"已处理: {word}")
                        else:
                            print(f"警告: 返回单词 {word} 不在请求列表中")

                    # 检查是否有缺失的单词
                    for word in batch:
                        if word not in results:
                            results[word] = {"error": f"API未返回该单词的结果: {word}"}
                            print(f"处理 {word} 时出错: API未返回结果")

                    # 成功处理当前批次，跳出重试循环
                    break

                elif response.status_code == 429:  # 速率限制
                    wait_time = 5 * (2 ** attempt) + random.uniform(0, 1)
                    print(f"速率限制，等待 {wait_time:.1f}秒后重试...")
                    time.sleep(wait_time)
                    continue

                else:
                    error_msg = f"API错误: {response.code} - {response.message}"
                    print(error_msg)
                    # 当前批次全部标记为错误
                    for word in batch:
                        results[word] = {"error": error_msg}
                    break

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"解析响应时出错: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"第 {attempt + 1} 次重试...")
                    continue
                else:
                    # 重试失败，标记当前批次为错误
                    for word in batch:
                        results[word] = {"error": f"解析响应失败: {str(e)}"}
            except Exception as e:
                print(f"未知错误: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"第 {attempt + 1} 次重试...")
                    time.sleep(1)
                    continue
                else:
                    for word in batch:
                        results[word] = {"error": str(e)}

    return results

# 使用示例
if __name__ == "__main__":
    API_KEY = "sk-15f426944d464eb4bd16a55f581232e1"

    # 示例单词列表
    words = ["sky", "occean", "mountain", "forest", "river"]

    # 批量处理单词
    words_data = batch_get_word_analysis(words, API_KEY)

    # 输出每个单词的详细信息
    for word in words:
        word_entry = words_data.get(word)
        if word_entry:
            print(f"\n=== {word} 的详细信息 ===")
            print(json.dumps(word_entry, indent=2, ensure_ascii=False))
        else:
            print(f"\n=== 未找到 {word} 的信息 ===")