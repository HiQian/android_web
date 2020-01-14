# coding=utf-8

import json

from data_item.items import WeiboItems

def param_card(card, item):
    # 获取card_type: 3:相关用户，9:微博用户，
    card_type = card.get('card_type') if 'card_type' in card else 0
    if card_type == 0:
        return
    if card_type == 9:
        itemid= card.get('itemid') if 'itemid' in card else None
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
            item['user_name'] = user.get('name') if user is not None and  'name' in user else None
            item['user_location'] = user.get('location') if user is not None and  'location' in user else None
            item['user_profile_url'] = 'https://weibo.com/' + user.get(
                'profile_url') if user is not None and  'profile_url' in user else None
            item['user_gender'] = user.get('gender') if user is not None and  'gender' in user else 'f'
            item['user_followers_count'] = user.get('followers_count') if user is not None and  'followers_count' in user else None
            item['user_created_at'] = user.get('created_at') if user is not None and  'created_at' in user else None
            # 解析page_info
            page_info = mblog.get('page_info')
            item['page_id'] = page_info.get('page_id') if page_info is not None and 'page_id' in page_info else None
            item['page_object_type'] = page_info.get('object_type') if page_info is not None and 'object_type' in page_info else None
            item['page_title'] = page_info.get('page_title') if page_info is not None and 'page_title' in page_info else None
            item['page_url'] = page_info.get('page_url') if page_info is not None and 'page_url' in page_info else None
    pass

content_text_json = None
with open("toutiao_data.json", 'r', encoding='utf-8') as f:
    content_text_json = json.loads(f.read(),)


if content_text_json:
    card_list = content_text_json.get('cards')
    for card in card_list:
        item = WeiboItems()
        param_card(card, item)
        print(item)