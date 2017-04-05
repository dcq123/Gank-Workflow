#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import os
from workflow import Workflow, ICON_WARNING, ICON_INFO, web

reload(sys)
sys.setdefaultencoding('utf8')

root_dir = "collect"

ICON_WEB = 'icon.png'


def change_type(query):
    t = None
    if query == "android":
        t = "Android"
    elif query == "ios":
        t = "iOS"
    elif query == "app":
        t = "App"
    elif query == "fuli":
        t = "福利"
    elif query == "video":
        t = "休息视频"
    elif query == "res":
        t = "拓展资源"
    elif query == "front":
        t = "前端"
    elif query == "other":
        t = "瞎推荐"
    return t


def not_more_input():
    title = "输入字符过少"
    subtitle = "请输入更多字符便于精确查找"
    wf.add_item(title, subtitle, valid=False, icon=ICON_WARNING)


def not_match_type():
    title = "查询提示"
    subtitle = "没有收藏该类型的干货数据"
    wf.add_item(title, subtitle, valid=False, icon=ICON_WARNING)


def not_end_input():
    title = "查询提示"
    subtitle = "输入完成后，已空格结尾触发查询"
    wf.add_item(title, subtitle, valid=False, icon=ICON_INFO)


def show_type(t):
    """
    打开指定类型的收藏文件
    """
    p = os.path.join('.', root_dir)
    filename = os.path.join(p, t + ".md")
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        return None


def main(wf):
    query = "Android "
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

    if query:
        query = query.strip()
        t = change_type(query)
        if t:
            filepath = show_type(t)
            if filepath is not None:
                wf.add_item(t + "干货", "按下Enter打开", arg="file:///" + filepath,
                            valid=True, icon=ICON_WEB)
                wf.send_feedback()
                return 0
    not_match_type()
    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
