# import pika
# import json

# credentials = pika.PlainCredentials('admin', '123456')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost',port = 5672,virtual_host = '/',credentials = credentials))
# channel=connection.channel()
# # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
# channel.exchange_declare(exchange = 'python-test',durable = True, exchange_type='fanout')
# for i in range(10):
#     message=json.dumps({'OrderId':"1000%s"%i})
# # 向队列插入数值 routing_key是队列名。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。routing_key 不需要配置
#     channel.basic_publish(exchange = 'python-test',routing_key = '',body = message,
#                           properties=pika.BasicProperties(delivery_mode = 2))
#     print(message)
# connection.close()

import pika
import json

# RabbitMQ 连接配置
credentials = pika.PlainCredentials('admin', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

# 声明 exchange
channel.exchange_declare(exchange='python-test', durable=True, exchange_type='fanout')

# 发送消息
def send_message(file_path, operation):
    message = {
        "file_path": file_path,
        "operation": operation
    }
    channel.basic_publish(
        exchange='python-test',
        routing_key='',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # 持久化消息
    )
    print(f"Sent message: {message}")

# 示例：发送提取 PDF 文本的任务
word_path = r'F:\大三下学期\移动应用开发\仓库\Muwu\文件处理\信息科学与工程学院实验报告模版.docx'
send_message(word_path, "convert_word_to_pdf")

# 关闭连接
connection.close()