from kafka import KafkaConsumer

consumer = KafkaConsumer('scrapy_weibo', bootstrap_servers=['10.142.112.29:9092'])
print(consumer.partitions_for_topic('scrapy_weibo'))
for message in consumer:
    print(message.value.decode(encoding='utf-8'))


