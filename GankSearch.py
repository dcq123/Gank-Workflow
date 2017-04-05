#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
from workflow import Workflow, ICON_WARNING, ICON_INFO, web

""" 查询【干货集中营】的数据 """
__author__ = "dcq"

reload(sys)
sys.setdefaultencoding('utf8')

# 某一天的干货数据
TODAY_URL = "http://gank.io/api/day/"
# 历史日期
HISTORY = "http://gank.io/api/day/history"
# 可选参数: Android | iOS | 休息视频 | 福利 | 拓展资源 | 前端 | 瞎推荐 | App
TYPE_URL = "http://gank.io/api/data/{type}/15/1"
# 按照关键字搜索
SEARCH_URL = "http://gank.io/api/search/query/{key}/category/all/count/15/page/1"

TYPE_ANDROID = "Android"
TYPE_IOS = "IOS"
TYPE_VIDEO = u"休息视频"
TYPE_OTHER = u"拓展资源"
TYPE_FULI = u"福利"

ICON_WEB = 'icon.png'


def get_type_data(key):
    """
    获取指定类型的Gank数据
    :return:
    """
    url = TYPE_URL.replace("{type}", key)
    r = web.get(url)

    # 如果请求失败，抛出错误信息
    r.raise_for_status()

    return r.json()


def get_key_data(q):
    """
    按关键字key查询匹配的数据
    :return:
    """
    url = SEARCH_URL.replace("{key}", q)
    r = web.get(url)

    # 如果请求失败，抛出错误信息
    r.raise_for_status()

    return r.json()


def get_history():
    """
    获取发布过的干货日期
    :return:
    """
    r = web.get(HISTORY)
    r.raise_for_status()
    rs = r.json()
    if not rs['error']:
        return rs['results'][0]


def get_last_data():
    """
    获取最近一次的干货数据
    :return:
    """
    last_day = get_history().replace('-', '/')
    r = web.get(TODAY_URL + last_day)

    # 如果请求失败，抛出错误信息
    r.raise_for_status()

    return r.json()

# 休息视频 | 福利 | 拓展资源 | 前端 | 瞎推荐


def change_type(query):
    t = None
    if query == "android":
        t = "Android"
    elif query == "ios":
        t = "iOS"
    elif query == "app":
        t = "App"
    elif query == "fuli":
        t = urllib.quote_plus("福利")
    elif query == "video":
        t = urllib.quote_plus("休息视频")
    elif query == "res":
        t = urllib.quote_plus("拓展资源")
    elif query == "front":
        t = urllib.quote_plus("前端")
    elif query == "other":
        t = urllib.quote_plus("瞎推荐")
    return t


def main(wf):
    query = None
    if len(wf.args):
        query = wf.args[0].replace("\\", "").lower()
        if len(query) > 0 and query[-1] != ' ':
            not_end_input()
            wf.send_feedback()
            return 0
        elif 0 < len(query) < 3:
            not_more_input()
            wf.send_feedback()
            return 0
    # 解析参数，进行查询
    if query:
        query = query.strip()
        t = change_type(query)
        if t is None:
            js = wf.cached_data(query, get_key_data, 60 * 60, query)
        else:
            js = wf.cached_data(t, get_type_data, 60 * 60, t)
        if not parse_type_data(js):
            add_error_item()
    else:
        # 从缓存中获取数据，设置缓存最大时间：60s
        js = wf.cached_data('data', get_last_data, max_age=60 * 60)
        if not parse_data(js):
            add_error_item()

    # Send the results to Alfred as XML
    wf.send_feedback()


def parse_type_data(js):
    if not js['error']:
        rs = js['results']
        if len(rs) == 0:
            return False
        for item in rs:
            add_item(item)
        return True
    else:
        return False


def parse_data(js):
    if not js['error']:
        rs = js['results']
        if len(rs) == 0:
            return False
        if TYPE_ANDROID in rs:
            for item in rs[TYPE_ANDROID]:
                add_item(item)
        if TYPE_IOS in rs:
            for item in rs[TYPE_IOS]:
                add_item(item)
        if TYPE_VIDEO in rs:
            for item in rs[TYPE_VIDEO]:
                add_item(item)
        if TYPE_OTHER in rs:
            for item in rs[TYPE_OTHER]:
                add_item(item)
        if TYPE_FULI in rs:
            for item in rs[TYPE_FULI]:
                add_item(item)

        return True
    else:
        return False


def add_item(item):
    if not item:
        return
    title = item['desc']
    createdAt = item['publishedAt'][0:10]
    subtitle = "[" + item['type'] + "]    by " + \
        (item['who'] if item['who'] is not None else "Null") + \
        "   " + createdAt
    image = "Null"
    if 'images' in item and item['images'] is not None:
        image = item['images'][0]
    elif u'福利' == item['type']:
        image = item['url']
    arg = item['type'] + '$' + title + '$' + item['url'] + '$' + image
    wf.add_item(title=title, subtitle=subtitle, arg=arg,
                valid=True, icon=ICON_WEB)


def add_error_item():
    title = "查询不到结果"
    subtitle = "请尝试其他关键字"
    wf.add_item(title, subtitle, valid=False, icon=ICON_WARNING)


def not_more_input():
    title = "输入字符过少"
    subtitle = "请输入更多字符便于精确查找"
    wf.add_item(title, subtitle, valid=False, icon=ICON_WARNING)


def not_end_input():
    title = "查询提示"
    subtitle = "输入完成后，已空格结尾触发查询"
    wf.add_item(title, subtitle, valid=False, icon=ICON_INFO)


if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
