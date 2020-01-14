# coding=utf-8
import json

from mitmproxy.http import HTTPFlow
from mitmproxy.net.http import headers
import sys, os
from mitmproxy.http import HTTPFlow
from mitmproxy import ctx
from kafka import KafkaProducer
import logging
import random
# BASE_DIR = 'D:\\project\\pythonProj\\andriod_web'
BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)
from data_item.items import WeiboItems


class BaseMintSearch(object):
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)  # Log等级开关

    path = '../log'
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)
        print('创建' + path)
    else:
        print('文件夹存在')

    log_name = path +'/log.log'
    logfile = log_name
    file_handler = logging.FileHandler(logfile, mode='a+')
    file_handler.setLevel(logging.ERROR)  # 输出到file的log等级的开关

    #定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)

    # 将handler添加到logger里面
    logger.addHandler(file_handler)

    # 如果需要同時需要在終端上輸出，定義一個streamHandler
    print_handler = logging.StreamHandler()  # 往屏幕上输出
    print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
    logger.addHandler(print_handler)

    def __init__(self, url_pattern, server='localhost:9092', topic='test'):
        self.num = 0
        self.url_pattrn = url_pattern
        self.logger = BaseMintSearch.logger
        self.server = server
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.server)
        self.partition = set()
        self.kafka_check('kafka_check')
        pass

    def __del__(self):
        if self.producer is not None:
            self.producer.close(5)

    def request(self, flow: HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("Weve seen %d flows" % self.num)

    def response(self, flow: HTTPFlow):
        pass

    def kafka_check(self, test_data):
        self.producer = KafkaProducer(bootstrap_servers=self.server)
        self.partition = self.producer.partitions_for(self.topic)
        print('host:'+self.server+' topic:'+self.topic+' 可用partiton' + str(self.producer.partitions_for(self.topic)))
        for partiton in self.partition:
            info = self.producer.send(topic=self.topic, value=test_data.encode('utf-8'), partition=partiton).get(5)
            print('当前partition:{}, offset:{}'.format(partiton, info.offset))
        # producer.close()


class WeiBoSearch(BaseMintSearch):

    def __init__(self, url_pattern, server='localhost:9092', topic='test'):
        super().__init__(url_pattern, server, topic)

    def response(self, flow: HTTPFlow):
        if flow.request.url.startswith(self.url_pattrn):
            # 获取文本编码
            enc = headers.parse_content_type(flow.response.headers.get("content-type", "")) or ("text", "plain", {})
            # 数据加载成json类
            content_text_json = json.loads(flow.response.text)
            card_list = content_text_json.get('cards')

            for card in card_list:
                item = WeiboItems()
                try:
                    self._param_card(card, item)
                    item_dic = dict(item)
                    jstr = json.dumps(item_dic, ensure_ascii=False)
                    if jstr != '{}':
                        self.producer.send(topic=self.topic, value=jstr.encode('utf-8'), partition=random.choice(list(self.partition)))
                except Exception as err:
                    self.logger.error(str(err.with_traceback()))
                print(item)

    def _param_card(self, card, item):
        # 获取card_type: 3:相关用户，9:微博用户，
        card_type = card.get('card_type') if 'card_type' in card else 0
        if card_type == 0:
            return
        if card_type == 9:
            itemid = card.get('itemid') if 'itemid' in card else None
            # 获取博客json
            mblog = card.get('mblog') if 'mblog' in card else None
            # 获取 mblog信息
            if mblog is not None:
                item['itemid'] = itemid
                item['title'] = mblog.get('title').get('text') if 'title' in mblog else None
                item['mid'] = mblog.get('mid') if 'mid' in mblog else None
                item['text'] = mblog.get('text') if 'text' in mblog else None
                item['source_type'] = mblog.get('source_type') if 'source_type' in mblog else None
                item['appid'] = mblog.get('appid') if 'appid' in mblog else None
                item['reposts_count'] = mblog.get('reposts_count') if 'reposts_count' in mblog else 0
                item['comments_count'] = mblog.get('comments_count') if 'comments_count' in mblog else 0
                item['attitudes_count'] = mblog.get('attitudes_count') if 'attitudes_count' in mblog else 0
                item['mblog_vip_type'] = mblog.get('mblog_vip_type') if 'mblog_vip_type' in mblog else 0
                # 解析user
                user = mblog.get('user')
                item['user_id'] = user.get('id') if user is not None and 'id' in user else None
                item['user_name'] = user.get('name') if user is not None and 'name' in user else None
                item['user_location'] = user.get('location') if user is not None and 'location' in user else None
                item['user_profile_url'] = 'https://weibo.com/' + user.get(
                    'profile_url') if user is not None and 'profile_url' in user else None
                item['user_gender'] = user.get('gender') if user is not None and 'gender' in user else 'f'
                item['user_followers_count'] = user.get(
                    'followers_count') if user is not None and 'followers_count' in user else None
                item['user_created_at'] = user.get('created_at') if user is not None and 'created_at' in user else None
                # 解析page_info
                page_info = mblog.get('page_info')
                item['page_id'] = page_info.get('page_id') if page_info is not None and 'page_id' in page_info else None
                item['page_object_type'] = page_info.get(
                    'object_type') if page_info is not None and 'object_type' in page_info else None
                item['page_title'] = page_info.get(
                    'page_title') if page_info is not None and 'page_title' in page_info else None
                item['page_url'] = page_info.get(
                    'page_url') if page_info is not None and 'page_url' in page_info else None
        pass


class TouiaoSerach(BaseMintSearch):
    def __init__(self, url_pattern, server='localhost:9092', topic='test'):
        super().__init__(url_pattern, server, topic)

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
                    jstr = json.dumps(item, ensure_ascii=False)
                    print(jstr)
                    jstr = json.dumps(item, ensure_ascii=False)
                    try:
                        self.producer.send(topic=self.topic, value=jstr.encode(encoding='utf-8'), partition=random.choice(list(self.partition)))
                    except:
                        self.logger.error('kafka 发送失败')
                    pass
                else:
                    continue
            pass
        pass

# 微博综合搜索url
weibo_search_url_pattern = 'https://api.weibo.cn/2/searchall?'
server = '10.142.112.29:9092'
topic = 'scrapy_weibo'
# 头条推荐栏url
toutiao_search_url_pattern = 'https://is-hl-ipv6.snssdk.com/api/news/feed/v88/?'
addons = [
    # WeiBoSearch(weibo_search_url_pattern, server, topic),
    TouiaoSerach(toutiao_search_url_pattern, server, topic)
]

# if __name__ == '__main__':
#     weibo_search_url_pattern = 'https://api.weibo.cn/2/searchall?'
#     server = '10.142.112.29:9092'
#     topic = 'scrapy_weibo'
#
#     toutiao = WeiBoSearch(weibo_search_url_pattern, server, topic)
#     toutiao.kafka_check('toutiao test')


