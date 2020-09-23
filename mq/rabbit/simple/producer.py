import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 相当于mq的控制对象
channel = connection.channel()
# 创建队列(非持久化)
queue_name = 'demo'
channel.queue_declare(queue=queue_name)

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body='Hello World!333')

# 创建队列(durable=True，使队列具备数据持久化能力)
queue_name2 = 'demo2'
channel.queue_declare(queue=queue_name2, durable=True)

channel.basic_publish(exchange='',
                      routing_key=queue_name2,
                      body='Hello World!333',
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      )
                      )
print("Sent 'Hello World!'")
connection.close()
