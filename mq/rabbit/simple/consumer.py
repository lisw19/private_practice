import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 创建队列
queue_name = 'demo'
channel.queue_declare(queue=queue_name)


def callback(ch, method, properties, body):
    print("Received %r" % body)
    # 手动应答模式，返回验证成功信息
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name,
                      auto_ack=False,  # 默认应答(可能存在数据丢失)/False 手动应答
                      on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
# 开始消费，开始监听
channel.start_consuming()
