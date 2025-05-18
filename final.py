import clip
import paddlehub as hub
import shutil
import cv2
import pika
import json
import os
import socket
import threading
import qrcode
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PIL import Image
import comtypes
import comtypes.client
import pdfplumber
import pytesseract
from spire.pdf import PdfDocument
from spire.pdf import FileFormat
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import subprocess
import sys



# RabbitMQ 连接配置
credentials = pika.PlainCredentials('admin', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

# 声明 exchange
channel.exchange_declare(exchange='python-test', durable=True, exchange_type='fanout')

base_url = f"https://511b136e.r21.cpolar.top"

def extract_pdf_text(pdf_path):
    """提取PDF文本并写入文件"""
    try:
        base_name = os.path.splitext(pdf_path)[0]
        output_path = f"{base_name}_extracted.txt"

        with pdfplumber.open(pdf_path) as pdf, \
             open(output_path, 'w', encoding='utf-8') as f:
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    f.write(f"=== 第 {page_num} 页内容 ===\n")
                    f.write(text + "\n\n")
                else:
                    f.write(f"=== 第 {page_num} 页无文本内容 ===\n\n")
            
            print(f"PDF文本已提取到：{output_path}")
            return output_path
    except Exception as e:
        print(f"提取PDF文本失败：{e}")
        return None

def is_rich_text(image_path):
    """判断图片是否为富文本"""
    try:
        with Image.open(image_path) as img:
            # 图像预处理（灰度 + 二值化）
            img = img.convert('L').point(lambda x: 0 if x < 180 else 255)
            
            # 执行OCR识别
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')

            text_length = len(text.replace(' ', '').replace('\n', ''))

            if text_length > 100:
                return True
            else:
                return False
            
    except Exception as e:
        print(f"判断图片是否为富文本失败：{e}")
        return False
def OCR(image_path):
    """执行OCR识别并写入文件"""
    
    dist_path = r'F:\image.png'

    try:
        shutil.copy(image_path, dist_path) 

        ocr = hub.Module(name="ch_pp-ocrv3", enable_mkldnn=True)
        result = ocr.recognize_text(images=[cv2.imread(dist_path)])

        # 生成输出路径
        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}_ocr.txt"

        extracted_texts = [item['text'] for item in result[0]['data']]
        text_content = '\n'.join(extracted_texts)  # 用换行符连接成字符串
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"OCR结果已保存到：{output_path}")

        results = {
            "text": text_content,
            "output_path": output_path
        }

        print(results)

        return results
    
    except Exception as e:
        print(f"OCR处理失败：{e}")
        return None

def convert_word_to_pdf(word_file_path):
    # 定义Word保存为PDF的格式常量
    wdFormatPDF = 17

    # 检查文件是否存在
    if not os.path.exists(word_file_path):
        print(f"文件不存在: {word_file_path}")
        return None

    # 检查文件扩展名是否为.doc或.docx
    if not word_file_path.endswith(('.doc', '.docx')):
        print("仅支持.doc或.docx格式文件")
        return None

    # 创建输出PDF文件路径（替换扩展名为.pdf）
    pdf_file_path = os.path.splitext(word_file_path)[0] + '.pdf'

    try:
        # 创建Word应用程序对象
        word_app = comtypes.client.CreateObject('Word.Application')
        word_app.Visible = False  # 隐藏Word界面

        # 打开Word文档
        doc = word_app.Documents.Open(word_file_path)
        
        # 保存为PDF格式
        doc.SaveAs(pdf_file_path, FileFormat=wdFormatPDF)
        
        # 关闭文档和应用程序
        doc.Close()
        word_app.Quit()

        print(f"转换成功: {word_file_path} -> {pdf_file_path}")
        return pdf_file_path  # 返回生成的PDF路径

    except Exception as e:
        print(f"转换失败: {e}")
        # 确保异常时关闭Word进程（即使出错也要尝试退出）
        try:
            word_app.Quit()
        except:
            pass
        return None

def pdf_to_word(pdf_file_path):
    try:
        pdf = PdfDocument()
        pdf.LoadFromFile(pdf_file_path)
        output_path = os.path.splitext(pdf_file_path)[0] + '.docx'
        pdf.SaveToFile(output_path, FileFormat.DOCX)
        return output_path
    except Exception as e:
        print(f"PDF转换失败：{e}")
        return None


# 将图像与文本描述进行匹配，返回最匹配的描述及其概率
def match_image_to_text(text_descriptions, image_path):
    
    # 加载设备配置
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 加载模型和预处理函数
    model, preprocess = clip.load("ViT-B/32", device=device, jit=False)

    # 尝试加载自定义权重（可选）
    try:
        model.load_state_dict(torch.load("vit-b-32.pth", map_location=device))
        print("成功加载自定义权重文件 'vit-b-32.pth'")
    except Exception as e:
        print(f"加载 'vit-b-32.pth' 失败: {e}，将使用默认预训练权重")

    print(image_path)

    # 加载和预处理图像
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    # 生成文本token并移动到设备
    text_inputs = torch.cat([clip.tokenize(desc) for desc in text_descriptions]).to(device)
    
    # 计算特征相似度
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
        top_prob, top_idx = similarity[0].topk(1)
    
    return text_descriptions[top_idx.item()], top_prob.item()

def generate_caption(image_path, condition_text="a photography of"):

    processor = BlipProcessor.from_pretrained(r"F:\大三下学期\移动应用开发\图片字幕\model")
    model = BlipForConditionalGeneration.from_pretrained(r"F:\大三下学期\移动应用开发\图片字幕\model")

    try:
        # 验证文件存在性
        if not os.path.exists(image_path):
            return f"错误：文件不存在 - {image_path}"
            
        # 加载并转换图像
        raw_image = Image.open(image_path).convert('RGB')
        
        # 图像描述生成
        inputs = processor(raw_image, condition_text, return_tensors="pt")
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
        
    except (IOError, OSError) as e:
        return f"图像处理失败: {str(e)}"
    except Exception as e:
        return f"未知错误: {str(e)}"

# 二维码相关函数
def get_local_ip():
    """获取本机IP地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要真正连接
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def start_server(port, directory):
    """启动HTTP服务器"""
    # 切换到指定目录
    os.chdir(directory)
    
    # 创建服务器
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("", port), handler)
    
    print(f"服务器启动在 http://{get_local_ip()}:{port}")
    httpd.serve_forever()

def generate_qrcode(url, filename, output_dir="qrcodes"):
    """生成包含文件URL的二维码"""
    # 确保输出目录存在（使用绝对路径）
    output_dir = os.path.abspath(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成唯一的二维码文件名
    timestamp = int(time.time())
    # 移除文件名中可能包含的路径分隔符，只保留文件名部分
    safe_filename = os.path.basename(filename.replace('/', '_').replace('\\', '_'))
    qrcode_filename = f"{safe_filename}_{timestamp}.png"
    output_path = os.path.join(output_dir, qrcode_filename)
    
    file_url = f"{url}/{filename}"
    img = qrcode.make(file_url)
    img.save(output_path)
    print(f"二维码已生成: {output_path}")
    print(f"二维码内容: {file_url}")
    return output_path

def create_file_qrcode(file_path, server_directory=None, port=8000):
    try:
        # 如果未指定服务器目录，使用文件所在目录
        if server_directory is None:
            server_directory = os.path.dirname(os.path.abspath(file_path))
        else:
            server_directory = os.path.abspath(server_directory)
            
        # 检查文件是否存在
        abs_file_path = os.path.abspath(file_path)
        if not os.path.exists(abs_file_path):
            return {
                "status": "failure",
                "message": f"文件不存在: {file_path}"
            }
            
        # 检查文件是否在服务器根目录下
        if not abs_file_path.startswith(server_directory):
            return {
                "status": "failure",
                "message": f"文件不在服务器根目录 '{server_directory}' 下"
            }
            
        # 计算相对于服务器根目录的路径
        rel_path = os.path.relpath(abs_file_path, server_directory)
        # 统一使用正斜杠作为URL路径分隔符
        filename = rel_path.replace('\\', '/')
        
        # 检查服务器是否已经运行
        server_running = False
        for thread in threading.enumerate():
            if thread.name == "qrcode_server":
                server_running = True
                break
                
        # 如果服务器未运行，启动新的服务器
        if not server_running:
            server_thread = threading.Thread(
                target=start_server, 
                args=(port, server_directory),
                name="qrcode_server"
            )
            server_thread.daemon = True
            server_thread.start()
            time.sleep(1)
            
        # 生成二维码
        qrcode_dir = os.path.join(os.getcwd(), "qrcodes")
        qrcode_path = generate_qrcode(base_url, filename, qrcode_dir)
        
        return {
            "status": "success",
            "qrcode_path": qrcode_path,
            "url": f"{base_url}/{filename}",
            "server_address": f"{base_url}"
        }
        
    except Exception as e:
        return {
            "status": "failure",
            "message": f"生成二维码失败: {str(e)}"
        }
    
def process_markdown_file(input_path, output_dir):
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist")
        return False
    
    input_dir = os.path.dirname(input_path)
    input_filename = os.path.basename(input_path)
    filename_without_ext = os.path.splitext(input_filename)[0]
    
    if output_dir is None:
        output_dir = input_dir
    
    os.makedirs(output_dir, exist_ok=True)
    
    html_file_path = os.path.join(output_dir, f"{filename_without_ext}.html")
    
    print(f"Processing Markdown file: {input_path}")
    print(f"Output HTML will be saved to: {html_file_path}")
        
    try:
        markdown_cmd = f"markmap \"{input_path}\" --output \"{html_file_path}\" --no-open"
        
        if os.name == 'nt':
            markdown_cmd = f"powershell -Command markmap \"{input_path}\" --output \"{html_file_path}\" --no-open"
        
        print(f"Executing command: {markdown_cmd}")
        
        result = subprocess.run(
            markdown_cmd,
            check=True, 
            text=True, 
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )
        
        print(f"Command return code: {result.returncode}")
        print(f"Command output: {result.stdout}")
        
        if result.returncode != 0:
            print(f"Command error: {result.stderr}")
            return False
        
        print(f"Successfully converted Markdown to HTML mindmap: {html_file_path}")
        return {
            "status": "success",
            "html_path": html_file_path
        }
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating HTML file: {e.output}\n{e.stderr}")
        return {
            "status": "failure",
            "result": f"Error generating HTML file: {e.output}\n{e.stderr}"
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            "status": "failure",
            "result": f"Unexpected error: {str(e)}"
        }


def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode('utf-8'))
        file_path = message.get("file_path")
        operation = message.get("operation")
        reply_to = properties.reply_to
        print(f"\n收到处理请求：{message}")

        # 执行对应操作
        if operation == "extract_pdf_text":
            result_path = extract_pdf_text(file_path)
            response = {
                "status": "success" if result_path else "failure",
                "result": result_path or "无输出",
                "file_path": file_path
            }
        elif operation == "OCR":
            results = OCR(file_path)
            response = {
                "status": "success" if results else "failure",
                "result": results.get("text") if results else "无输出",
                "file_path": results.get("output_path") if results else "无输出"
            }
        elif operation == "convert_word_to_pdf":
            result_path = convert_word_to_pdf(file_path)
            response = {
                "status": "success" if result_path else "failure",
                "result": result_path or "无输出",
                "file_path": file_path
            }
        elif operation == "pdf_to_word":
            result_path = pdf_to_word(file_path)
            response = {
                "status": "success" if result_path else "failure",
                "result": result_path or "无输出",
                "file_path": file_path
            }
        elif operation == "is_rich_text":
            result = is_rich_text(file_path)
            response = {
                "status": "success" if result else "failure",
                "result": result or False,
            }
        elif operation == "get_photo_tag":
            text_descriptions = message.get("text_descriptions")
            result = match_image_to_text(text_descriptions, file_path)
            response = {
                "status": "success" if result else "failure",
                "result": result[0],
            }
        elif operation == "generate_caption":
            result = generate_caption(file_path)
            response = {
                "status": "success" if result else "failure",
                "result": result or "无输出",
            }
        elif operation == "create_file_qrcode":
            server_directory = message.get("server_directory")
            port = message.get("port", 8000)
            result = create_file_qrcode(file_path, server_directory, port)
            response = result
        elif operation == "Generate_mindmap":
            output_dir = message.get("output_dir")
            response = process_markdown_file(file_path, output_dir)
        else:
            print(f"不支持的操作类型：{operation}")
            response = {
                "status": "failure",
                "result": "不支持的操作类型"
            }

        # # 记录处理日志
        # with open("processing_log.txt", "a", encoding='utf-8') as log_file:
        #     status = "成功" if result else "失败"
        #     log_entry = f"{operation} | {file_path} | {status} | {result or '无输出'}\n"
        #     log_file.write(log_entry)

        # 将结果发送到回调队列
        if reply_to:
            channel.basic_publish(
                exchange='',
                routing_key=reply_to,
                body=json.dumps(response),
                properties=pika.BasicProperties(delivery_mode=2)  # 持久化
            )
            print(f"结果已发送到回调队列: {reply_to}")
        else:
            print("没有回调队列，无法返回结果")

    except Exception as e:
        print(f"消息处理异常：{e}")
        # 发送错误信息
        if properties.reply_to:
            channel.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                body=json.dumps({"status": "error", "message": str(e)})
            )
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    # 创建日志文件
    if not os.path.exists("processing_log.txt"):
        open("processing_log.txt", "w").close()
        
    # 启动消费者
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='python-test', queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print('等待处理请求，按 CTRL+C 退出...')
    channel.start_consuming()