


import sys,os
BASE_DIR = 'D:\\project\\pythonProj\\andriod_web'
sys.path.append(BASE_DIR)
from data_item.items import WeiboItems

if __name__ == '__main__':
    item = WeiboItems()
    item['itemid'] = '张三'
    print(item)