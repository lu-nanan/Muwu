# import pika

# credentials = pika.PlainCredentials('admin', '123456')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost',port = 5672,virtual_host = '/',credentials = credentials))
# channel = connection.channel()
# # 创建临时队列,队列名传空字符，consumer关闭后，队列自动删除
# result = channel.queue_declare('',exclusive=True)
# # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
# channel.exchange_declare(exchange = 'python-test',durable = True, exchange_type='fanout')
# # 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去
# channel.queue_bind(exchange = 'python-test',queue = result.method.queue)
# # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
# def callback(ch, method, properties, body):
#     ch.basic_ack(delivery_tag = method.delivery_tag)
#     print(body.decode())

# channel.basic_consume(result.method.queue,callback,# 设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
#                       auto_ack = False)
# channel.start_consuming()

import pika
import json
import pdfplumber

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

# 提取 PDF 文本的函数
def extract_pdf_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    print(f"Extracted text from {pdf_path}:\n{text}")
                else:
                    print(f"No text found on a page in {pdf_path}")
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")

# 消费者回调函数
def callback(ch, method, properties, body):
    try:
        # 解析消息
        message = json.loads(body.decode('utf-8'))
        file_path = message.get("file_path")
        operation = message.get("operation")

        print(f"Received message: {message}")

        # 根据操作类型执行任务
        if operation == "extract_pdf_text":
            extract_pdf_text(file_path)
            print("PDF text extraction completed.")
        else:
            print(f"Unsupported operation: {operation}")

    except Exception as e:
        print(f"Error processing message: {e}")

    # 确认消息已处理
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 开始消费消息
channel.basic_consume(queue=queue_name, on_message_callback=callback)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()