#coding=utf8

from kafka import KafkaProducer

if __name__ == '__main__':
    server = '10.142.112.29:9092'
    topic = 'scrapy_weibo'
    producer = KafkaProducer(bootstrap_servers=server)
    producer.send(topic=topic, value="hello kafka".encode())
    producer.close()
