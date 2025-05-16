import ast
import clip
import paddlehub as hub
import shutil
import cv2
import pika
import json
import os
from PIL import Image
import comtypes
import comtypes.client
import pdfplumber
import pytesseract
from spire.pdf import PdfDocument
from spire.pdf import FileFormat
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# RabbitMQ 连接配置
credentials = pika.PlainCredentials('admin', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

# 声明 exchange
channel.exchange_declare(exchange='python-test', durable=True, exchange_type='fanout')

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
        return output_path
    
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
            result_path = OCR(file_path)
            response = {
                "status": "success" if result_path else "failure",
                "result": result_path or "无输出",
                "file_path": file_path
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
                "result": result or "无输出",
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