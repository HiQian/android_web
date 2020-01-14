# coding=utf-8

from . import base_item


class WeiboItems(base_item.Item):
    itemid = base_item.Field()
    title = base_item.Field()
    mid = base_item.Field()
    text = base_item.Field()
    source_type = base_item.Field()
    appid = base_item.Field()
    reposts_count = base_item.Field()
    comments_count = base_item.Field()
    attitudes_count = base_item.Field()
    mblog_vip_type = base_item.Field()
    user_id = base_item.Field()
    user_name = base_item.Field()
    user_location = base_item.Field()
    user_profile_url = base_item.Field()
    user_gender = base_item.Field()
    user_followers_count = base_item.Field()
    user_created_at = base_item.Field()
    page_id = base_item.Field()
    page_object_type = base_item.Field()
    page_title = base_item.Field()
    page_url = base_item.Field()