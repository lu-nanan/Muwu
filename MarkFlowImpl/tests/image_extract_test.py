import os
import base64
import requests
import json


class ImageRecognitionTester:
    """图像识别测试工具类，专门用于测试通义千问的 qwen-vl-max 模型"""

    @staticmethod
    def test_qwen_vl_max(image_path, api_key):
        """
        使用通义千问的 qwen-vl-max 模型测试图像识别功能

        参数:
            image_path: 图片文件路径
            api_key: API密钥

        返回:
            包含识别结果的字典
        """
        # 检查图片文件是否存在
        if not os.path.exists(image_path):
            return {
                'success': False,
                'error': f'图片文件不存在: {image_path}'
            }

        try:
            # 读取图片文件
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # 将图片转换为base64编码
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            # 使用通义千问的多模态API端点
            api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

            # 构建API请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            # qwen-vl-max 模型的请求格式
            payload = {
                "model": "qwen-vl-max",
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "image": f"data:image/jpeg;base64,{image_base64}"
                                },
                                {
                                    "text": "这是一张英语短文的图片，其中有一些被红色记号笔覆盖的单词。请识别出所有被红色覆盖的单词，仅返回单词列表，不要其他解释。格式为：['word1', 'word2', ...]"
                                }
                            ]
                        }
                    ]
                },
                "parameters": {
                    "incremental_output": False
                }
            }

            # 打印请求信息以便调试
            print("请求头:", headers)
            print("请求体预览:", json.dumps(payload, indent=2, ensure_ascii=False)[:500] + "...")

            # 发送请求到API
            print("正在发送请求到API...")
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            # 检查响应状态
            print(f"响应状态码: {response.status_code}")

            # 如果请求失败，尝试获取更多错误信息
            if response.status_code != 200:
                error_detail = response.text
                print(f"错误详情: {error_detail}")
                response.raise_for_status()

            # 解析API响应
            result = response.json()
            print(f"API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

            # 提取并处理结果
            if 'output' in result and 'choices' in result['output'] and len(result['output']['choices']) > 0:
                # 注意：返回的content是一个列表，列表中的元素是字典，包含text字段
                content_list = result['output']['choices'][0]['message']['content']
                # 将content列表中的所有文本内容合并
                text_response = ""
                for content_item in content_list:
                    if 'text' in content_item:
                        text_response += content_item['text'] + " "
                text_response = text_response.strip()

                # 如果没有提取到文本，则使用整个content列表的字符串表示
                if not text_response:
                    text_response = str(content_list)

                covered_words = ImageRecognitionTester.parse_covered_words_from_text(text_response)
            else:
                covered_words = []

            return {
                'success': True,
                'covered_words': covered_words,
                'raw_response': result,
                'message': '识别成功'
            }

        except requests.exceptions.RequestException as e:
            # 获取更多错误信息
            error_msg = f'API请求失败: {str(e)}'
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg += f"\n错误详情: {json.dumps(error_detail, indent=2, ensure_ascii=False)}"
                except:
                    error_msg += f"\n响应文本: {e.response.text}"
            print(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f'处理过程中发生错误: {str(e)}'
            print(error_msg)
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': error_msg
            }

    @staticmethod
    def parse_covered_words_from_text(text):
        """
        从API返回的文本中解析出被覆盖的单词列表

        参数:
            text: API返回的文本内容

        返回:
            被覆盖的单词列表
        """
        print(f"解析文本: {text}")

        # 处理可能的JSON数组格式
        try:
            # 尝试直接解析为JSON
            if text.startswith('[') and text.endswith(']'):
                words = json.loads(text)
                if isinstance(words, list):
                    return words
        except json.JSONDecodeError:
            # 如果不是有效的JSON，继续尝试其他解析方式
            pass

        # 处理可能的字符串列表格式
        try:
            # 处理类似 "['word1', 'word2']" 的格式
            if text.startswith('[') and text.endswith(']'):
                # 移除方括号和引号
                text = text.strip('[]').replace("'", "").replace('"', "")
                words = [word.strip() for word in text.split(',') if word.strip()]
                return words
        except Exception as e:
            print(f"解析单词列表出错: {e}")

        # 如果以上方法都失败，尝试基于关键词解析
        covered_words = []
        keywords = ["被覆盖的单词有:", "covered words:", "单词:", "words:"]

        for keyword in keywords:
            if keyword in text:
                # 提取关键词后面的内容
                words_part = text.split(keyword)[1].strip()
                # 去除可能的多余文本
                if "\n" in words_part:
                    words_part = words_part.split("\n")[0]

                # 分割单词
                words = words_part.split(",")
                covered_words = [word.strip() for word in words if word.strip()]
                break

        return covered_words


# 使用示例
if __name__ == "__main__":
    # 设置API信息
    API_KEY = "sk-15f426944d464eb4bd16a55f581232e1"  # 替换为您的API密钥
    IMAGE_PATH = "D:/software/PyCharm/PythonProject/MarkFlow/Screenshot_20250908_102429_com.huawei.hinote.png"  # 替换为您的图片路径

    # 测试图像识别
    result = ImageRecognitionTester.test_qwen_vl_max(
        image_path=IMAGE_PATH,
        api_key=API_KEY
    )

    # 打印结果
    print("\n识别结果:")
    print(f"成功: {result['success']}")
    if result['success']:
        print(f"被覆盖的单词: {result['covered_words']}")
    else:
        print(f"错误: {result['error']}")