# coding=utf-8

import json

if __name__ == '__main__':
    jstr = None
    with open('test.json', 'r', encoding='utf-8') as f:
        load_dic = json.load(f)
    data_list = load_dic.get('data')
    for data in data_list:
        item = dict()
        # 获取数据content
        data_content = data.get('content')
        data_content_json = json.loads(data_content)
        # 判断时候为广告
        data_label = data_content_json.get('label') if 'label' in data_content_json else ""
        if data_label == '广告':
            item['display_url'] = data_content_json.get('display_url') if 'display_url' in data_content_json else ""
            large_image_list = data_content_json.get(
                'large_image_list') if 'large_image_list' in data_content_json else ""
            item['large_image_list_url'] = large_image_list[0].get(
                    'url') if large_image_list[0] is not None and 'url' in large_image_list[0] else ""
            item['title'] = data_content_json.get('title') if 'title' in data_content_json else ""
            item['source'] = data_content_json.get('source') if 'source' in data_content_json else ""
            jstr = json.dumps(item, ensure_ascii=False)
            print(jstr)
            pass