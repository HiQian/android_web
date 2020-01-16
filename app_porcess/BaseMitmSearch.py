# coding=utf-8
import json
from mitmproxy.net.http import headers
import sys, os
from mitmproxy.http import HTTPFlow
from mitmproxy import ctx
from kafka import KafkaProducer
import logging
import random
import time
BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)
from app_porcess.dbUtls import MysqlPool

pool = MysqlPool(host="10.144.15.187", port=3815, username='spider', passwd='QAZwsxEDC', db='spider')

class BaseMimtSearch(object):
    time_str = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级开关
    path = '../log'
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)
        print('创建' + path)
    log_name = path +'/'+'log '+time_str+'.log'
    logfile = log_name
    file_handler = logging.FileHandler(logfile, mode='a+')
    file_handler.setLevel(logging.INFO)  # 输出到file的log等级的开关
    #定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s ")
    file_handler.setFormatter(formatter)
    # 将handler添加到logger里面
    logger.addHandler(file_handler)
    # 如果需要同時需要在終端上輸出，定義一個streamHandler
    print_handler = logging.StreamHandler()  # 往屏幕上输出
    print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
    logger.addHandler(print_handler)

    def __init__(self, url_pattern, server='localhost:9092', topic='scrapy_weibo', meta_topic='test'):
        self.num = 0
        self.url_pattrn = url_pattern
        self.logger = BaseMimtSearch.logger
        self.server = server
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.server)
        self.kafka_check(server, topic, 'kafka_check')
        self.kafka_check(server, meta_topic, 'kafka_meta_check')
        self.meta_topic = meta_topic
        pass

    def __del__(self):
        if self.producer is not None:
            self.producer.close(5)

    def request(self, flow: HTTPFlow):
        self.num = self.num + 1
        ctx.log.warn("Weve seen %d flows" % self.num)
        # ctx.log.warn(str(flow.request.query))
        # ctx.log.error(str(flow.request.headers))

    def response(self, flow: HTTPFlow):
        pass

    def kafka_check(self, server, topic, test_data):
        producer = KafkaProducer(bootstrap_servers=server)
        partitions = producer.partitions_for(topic)
        self.logger.info('host:'+server+' topic:'+topic+' 可用partitons' + str(producer.partitions_for(topic)))
        for partiton in partitions:
            try:
                info = producer.send(topic=topic, value=test_data.encode('utf-8'), partition=partiton).get(5)
                self.logger.info(('当前host:{}, 当前topic:{}当前partition:{}, offset:{}'.format(server, topic, partiton, info.offset)))
            except:
                self.logger.error('could not send message to host:{}, topic:{}, partiton:{}.'.format(server, topic, partiton))


class TouiaoSerach(BaseMimtSearch):
    def __init__(self, url_pattern, server='localhost:9092', topic='scrapy_weibo', meta_topic='test'):
        super().__init__(url_pattern, server, topic, meta_topic)

    def response(self, flow: HTTPFlow):
        if flow.request.url.startswith(self.url_pattrn):
            # 获取文本编码
            enc = headers.parse_content_type(flow.response.headers.get("content-type", "")) or ("text", "plain", {})
            # 数据加载成json类
            content_text_json = json.loads(flow.response.text)
            data_list = content_text_json.get('data')
            for data in data_list:
                item = dict()
                # 获取数据content
                data_content = data.get('content')
                data_content_json = json.loads(data_content)
                # 判断时候为广告
                data_label = data_content_json.get('label') if 'label' in data_content_json else ""
                if data_label == '广告':
                    item['display_url'] = data_content_json.get(
                        'display_url') if 'display_url' in data_content_json else ""
                    large_image_list = data_content_json.get(
                        'large_image_list') if 'large_image_list' in data_content_json else ""
                    item['large_image_list_url'] = large_image_list[0].get(
                        'url') if large_image_list[0] is not None and 'url' in large_image_list[0] else ""
                    item['title'] = data_content_json.get('title') if 'title' in data_content_json else ""
                    item['source'] = data_content_json.get('source') if 'source' in data_content_json else ""
                    jstr = ""
                    try:
                        jstr = json.dumps(item, ensure_ascii=False)
                        meta_data = json.dumps(data_content_json, ensure_ascii=False)
                        self.producer.send(topic=self.topic, value=jstr.encode(encoding='utf-8'), partition=random.choice(list(self.producer.partitions_for(self.topic))))
                        self.producer.send(topic=self.meta_topic, value=data_content.encode(encoding='utf-8'), partition=random.choice(list(self.producer.partitions_for(self.meta_topic))))
                    except Exception as err:
                        self.logger.error('kafka send failure:host:{}, topic:{}, values:'.format(self.server, self.topic, jstr))
                    sql = 'insert into android_toutiao_app(meta_data, display_url, large_image_list, title, `source`, create_time) value (%s,%s,%s,%s,%s, %s);'
                    data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    args = (meta_data, item.get('display_url'), item.get('large_image_list_url'), item.get('title'), item.get('source'), data_time)
                    pool.insert(sql, args)
                else:
                    continue
            pass
        pass
