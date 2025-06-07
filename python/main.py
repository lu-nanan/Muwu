import pika
import json


from sr_extend import SR
from qrcode_extend  import generate_qr_code
from markdown_extend import process_markdown_file
from pdf_extend import *
from word_extend import convert_word_to_pdf
from photo_extend import OCR, generate_caption, is_rich_text, match_image_to_text


# with open('config.json', 'r', encoding='utf-8') as f:
#     config = json.load(f)

# rabbitmq_config = config['rabbitmq']


# base_url = config['base_url']
# blip_path = config['paths']['blip_model']
# vit_b_path = config['paths']['clip_model']
# gan_path = config['paths']['sr_model']
# sr_path = config['paths']['sr_model']
# temp_dist = config['paths']['temp_dist']


# RabbitMQ 连接配置
credentials = pika.PlainCredentials('admin', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, virtual_host='/', credentials=credentials))


# credentials = pika.PlainCredentials(
#     rabbitmq_config['username'], 
#     rabbitmq_config['password']
# )
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#     host=rabbitmq_config['host'], 
#     port=rabbitmq_config['port'], 
#     virtual_host=rabbitmq_config['virtual_host'], 
#     credentials=credentials
# ))

channel = connection.channel()

# 声明 exchange
channel.exchange_declare(exchange='python-test', durable=True, exchange_type='fanout')


# 文件服务器的端口地址对外的域名
base_url = f"https://63793dfe.r21.cpolar.top"

blip_path = r"F:\大三下学期\移动应用开发\图片字幕\model"

vit_b_path = r"F:\\大三下学期\\移动应用开发\\图片分类\\ViT-B-32.pth"

gan_path = r"F:\大三下学期\移动应用开发\仓库\srgan_generator_final.pth"

sr_path = r"F:\大三下学期\移动应用开发\仓库\srgan_generator_final.pth"

qr_path = r"F:\大三下学期\移动应用开发\仓库\Muwu\python\qrcode"

temp_dist = r"F:\image.png"

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
                "file_path": extract_pdf_text(result_path)
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
            result = match_image_to_text(text_descriptions, file_path, vit_b_path)
            response = {
                "status": "success" if result else "failure",
                "result": result[0],
            }
        elif operation == "generate_caption":
            result = generate_caption(file_path, blip_path)
            response = {
                "status": "success" if result else "failure",
                "result": result or "无输出",
            }
        elif operation == "create_file_qrcode":
            result = generate_qr_code(message.get("userId"), qr_path, message.get("url"))
            response = result
        elif operation == "Generate_mindmap":
            output_dir = message.get("output_dir")
            response = process_markdown_file(file_path, output_dir)
        elif operation == "SR":
            response = SR(file_path, sr_path)
        else:
            print(f"不支持的操作类型：{operation}")
            response = {
                "status": "failure",
                "result": "不支持的操作类型"
            }

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
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='python-test', queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print('等待处理请求，按 CTRL+C 退出...')
    channel.start_consuming()