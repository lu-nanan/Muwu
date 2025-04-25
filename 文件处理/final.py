import os
from PIL import Image  # 修正导入语句
import comtypes
import pika
import json
import pdfplumber
import pytesseract
import comtypes.client
from spire.pdf import PdfDocument
from spire.pdf import FileFormat


# RabbitMQ 连接配置
credentials = pika.PlainCredentials('admin', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

# 声明 exchange 和 queue
channel.exchange_declare(exchange='python-test', durable=True, exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='python-test', queue=queue_name)

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

def OCR(image_path):
    """执行OCR识别并写入文件"""
    try:
        # 配置Tesseract路径
        pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"
        
        # 打开并预处理图片
        with Image.open(image_path) as img:
            # 图像预处理（灰度 + 二值化）
            img = img.convert('L').point(lambda x: 0 if x < 180 else 255)
            
            # 执行OCR识别
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        # 生成输出路径
        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}_ocr.txt"
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
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
        return

    # 检查文件扩展名是否为.doc或.docx
    if not word_file_path.endswith(('.doc', '.docx')):
        print("仅支持.doc或.docx格式文件")
        return

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

def pdf_to_word(pdf_file_path)
    try:
        pdf = PdfDocument()
        pdf.LoadFromFile(pdf_file_path)
        output_path = os.path.splitext(pdf_file_path)[0] + '.docx'
        pdf.SaveToFile(output_path, FileFormat=FileFormat.DOCX)
        return output_path
    except Exception as e:
        print(f"PDF转换失败：{e}")
        return None
    
def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode('utf-8'))
        file_path = message.get("file_path")
        operation = message.get("operation")

        print(f"\n收到处理请求：{message}")

        # 执行对应操作
        if operation == "extract_pdf_text":
            result_path = extract_pdf_text(file_path)
        elif operation == "OCR":
            result_path = OCR(file_path)
        elif operation == "convert_word_to_pdf":
            result_path = convert_word_to_pdf(file_path)
        else:
            print(f"不支持的操作类型：{operation}")
            result_path = None

        # 记录处理日志
        with open("processing_log.txt", "a", encoding='utf-8') as log_file:
            status = "成功" if result_path else "失败"
            log_entry = f"{operation} | {file_path} | {status} | {result_path or '无输出'}\n"
            log_file.write(log_entry)

    except Exception as e:
        print(f"消息处理异常：{e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    # 创建日志文件
    if not os.path.exists("processing_log.txt"):
        open("processing_log.txt", "w").close()

    # 启动消费者
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print('等待处理请求，按 CTRL+C 退出...')
    channel.start_consuming()