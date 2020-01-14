
import os
path = '../log'
folder = os.path.exists(path)
if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
    os.makedirs(path)
    print('创建'+path)
else:
    print('文件夹存在')
