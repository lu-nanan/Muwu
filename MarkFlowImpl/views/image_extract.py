import base64
import json
import os
import ssl
from math import factorial

import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

import urllib3


# 通义千问API配置 - 请替换为你的实际配置
TONGYI_API_KEY = "sk-15f426944d464eb4bd16a55f581232e1"  # 你的通义千问API密钥
TONGYI_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@api_view(['POST'])
def recognize_covered_words(request):
    """处理前端上传的图片，使用通义千问-QVQ-Max识别被红色记号笔覆盖的单词"""
    if 'image' not in request.FILES:
        return JsonResponse({
            'success': False,
            'error': '未提供图片文件'
        }, status=400)

    image_file = request.FILES['image']

    try:
        # 读取上传的图片数据
        image_data = image_file.read()

        # 确保传递API密钥
        result = process_image_with_tongyi(image_data, TONGYI_API_KEY)

        # 将字典结果转换为JsonResponse
        return JsonResponse(result)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'success': False,
            'error': f'API请求失败: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'处理过程中发生错误: {str(e)}'
        }, status=500)

@api_view(['POST','GET'])
@csrf_exempt
def test_recognize_covered_words(request):
    """本地测试用接口，通过图片路径参数读取本地图片"""
    """本地测试用接口，通过图片路径参数读取本地图片"""
    # 根据请求方法获取参数
    if request.method == 'GET':
        image_path = request.query_params.get('image_path')
        print(f"GET参数 image_path: {image_path}")
    else:  # POST
        image_path = request.data.get('image_path')
        print(f"POST参数 image_path: {image_path}")

    if not image_path:
        return JsonResponse({'success': False, 'error': '请提供图片路径参数 image_path'}, status=400)

    # 2. 安全检查相关变量
    allowed_dirs = [os.path.abspath(settings.MEDIA_ROOT)]
    print(f"允许的目录: {allowed_dirs}")

    image_abs_path = os.path.abspath(image_path)
    print(f"图片绝对路径: {image_abs_path}")

    # 3. 检查路径是否在允许的目录内
    is_allowed = any(image_abs_path.startswith(allowed_dir) for allowed_dir in allowed_dirs)
    print(f"路径是否允许访问: {is_allowed}")

    if not is_allowed:
        return JsonResponse({
            'success': False,
            'error': f'图片路径不允许访问（允许的目录：{allowed_dirs}）'
        }, status=403)

    # 4. 检查文件是否存在
    if not os.path.exists(image_abs_path):
        return JsonResponse({
            'success': False,
            'error': f'图片文件不存在: {image_abs_path}'
        }, status=404)

    try:
        with open(image_abs_path, 'rb') as f:
            image_data = f.read()

        # 确保传递API密钥
        result = process_image_with_tongyi(image_data, TONGYI_API_KEY)

        # 将字典结果转换为JsonResponse
        return JsonResponse(result)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'success': False,
            'error': f'API请求失败: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'处理过程中发生错误: {str(e)}'
        }, status=500)


def process_image_with_tongyi(image_data, api_key):
    """
    使用通义千问的 qwen-vl-max 模型测试图像识别功能

    参数:
        image_data: 图片二进制数据
        api_key: API密钥

    返回:
        包含识别结果的字典
    """
    if not api_key:
        return {
            'success': False,
            'error': 'API密钥未配置'
        }

    try:
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

        # 发送请求到API
        print("正在发送请求到API...")

        # 尝试使用不同的SSL配置
        session = requests.Session()

        # 方法1: 尝试使用系统默认证书
        try:
            response = session.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
        except ssl.SSLError:
            # 方法2: 如果SSL错误，尝试不使用验证（仅用于测试环境）
            print("SSL错误，尝试不使用证书验证...")
            response = session.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=60,
                verify=False
            )

        # 检查响应状态
        print(f"响应状态码: {response.status_code}")

        if response.status_code != 200:
            error_detail = response.text
            print(f"错误详情: {error_detail}")
            return {
                'success': False,
                'error': f'API请求失败: {response.status_code} - {error_detail}'
            }

        # 解析API响应
        result = response.json()
        print(f"API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

        # 提取并处理结果
        covered_words = []
        if ('output' in result and
                'choices' in result['output'] and
                len(result['output']['choices']) > 0):

            # 获取响应内容
            content = result['output']['choices'][0]['message']['content']

            # 处理响应内容（可能是列表或字典）
            if isinstance(content, list):
                # 如果是列表，提取所有文本内容
                text_response = ""
                for item in content:
                    if 'text' in item:
                        text_response += item['text']
                covered_words = parse_covered_words_from_text(text_response)
            elif isinstance(content, str):
                # 如果是字符串，直接解析
                covered_words = parse_covered_words_from_text(content)

        return {
            'success': True,
            'covered_words': covered_words,
            #'raw_response': result,
            'message': '识别成功'
        }

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return {
            'success': False,
            'error': f'处理过程中发生错误: {str(e)}'
        }


def parse_covered_words_from_text(text):
    """
    从API返回的文本中解析出被覆盖的单词列表

    参数:
        text: API返回的文本

    返回:
        单词列表
    """
    # 尝试直接解析JSON格式的响应
    try:
        # 尝试找到文本中的JSON数组
        import re
        json_match = re.search(r'\[.*\]', text)
        if json_match:
            json_str = json_match.group()
            words = json.loads(json_str)
            if isinstance(words, list):
                return words
    except:
        pass

    # 如果JSON解析失败，尝试其他方法提取单词
    words = []

    # 方法1: 查找被引号包围的单词
    import re
    quoted_words = re.findall(r'[\'"](.*?)[\'"]', text)
    if quoted_words:
        return quoted_words

    # 方法2: 查找看起来像英文单词的序列
    word_pattern = r'\b[a-zA-Z]{2,}\b'
    potential_words = re.findall(word_pattern, text)

    # 过滤掉常见的不可能是被覆盖单词的词汇
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    filtered_words = [word for word in potential_words if word.lower() not in common_words]

    return filtered_words if filtered_words else potential_words