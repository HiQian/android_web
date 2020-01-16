#coding=utf-8

import xlwings
import time
from .BaseMitmSearch import pool

# chuang
app = xlwings.App(visible=False, add_book=False)
wb = app.books.add()
sheet = wb.sheets['Sheet1']
sql = 'select id, display_url, large_image_list, title, source, create_time from android_toutiao_app where create_time> DATE_SUB(now(),INTERVAL 24 HOUR ) and create_time<now() and is_read= false;'
data_dic = pool.fetch_all(sql)
# 存在数据再处理
if data_dic is not None:
    keys = list(data_dic[0].keys())
    sheet.range((1, 1), (1, len(keys))).value = keys
    row = 1
    for data in data_dic:
        row = row + 1
        data_list = list(data.values())
        sheet.range((row,1), (row, len(data_list))).value = data_list
        sheet.range((row,1), (row, len(data_list))).columns.autofit()
        sql = 'update android_toutiao_app set is_read=true where id=%s;'
        pool.update(sql,data.get('id'))
    data_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    wb.save('../log/'+data_time+'.xlsx')
wb.close()
app.quit()