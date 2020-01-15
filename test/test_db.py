import os, sys
BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)
from app_porcess.dbUtls import MysqlPool
import json
import time


if __name__ == '__main__':
    pool = MysqlPool(host="10.144.15.187", port=3815, username='spider', passwd='QAZwsxEDC', db='spider')
    jstr = '{"test":1}'
    jobj = json.dumps(jstr, ensure_ascii=False)
    item = dict(display_url="1", large_image_list_url="2", title="3", source="4")
    sql = 'insert into android_toutiao_app(meta_data, display_url, large_image_list, title, `source`, create_time) value (%s,%s,%s,%s,%s, %s);'
    data_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    args = (jstr, item.get('display_url'), item.get('large_image_list_url'), item.get('title'), item.get('source'), data_time)
    pool.insert(sql, args)