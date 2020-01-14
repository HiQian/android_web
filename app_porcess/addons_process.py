# coding=utf-8
import os,sys
BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)
from app_porcess.BaseMitmSearch import TouiaoSerach

weibo_search_url_pattern = 'https://api.weibo.cn/2/searchall?'
server = '10.142.112.29:9092'
topic = 'scrapy_weibo'
meta_topic = 'test'
# 头条推荐栏url
toutiao_search_url_pattern = 'https://is-hl-ipv6.snssdk.com/api/news/feed/v88/?'
addons = [
    # WeiBoSearch(weibo_search_url_pattern, server, topic),
    TouiaoSerach(toutiao_search_url_pattern, server, topic, meta_topic)
]