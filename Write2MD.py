#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys
import os
from workflow import Workflow
from markdownwriter.MarkdownWriter import MarkdownWriter

reload(sys)
sys.setdefaultencoding('utf8')

root_dir = "collect"


def write_md(item_type, title, url, image="Null"):
    p = os.path.join('.', root_dir)
    if not os.path.exists(p):
        os.makedirs(p)
    filename = os.path.join(p, item_type + ".md")
    md = MarkdownWriter()
    if not os.path.exists(filename):
        file = open(filename, 'w+')
        md.addHeader(item_type + '干货', 3)
        md.addParagraph("收集【干货集中营】中每天分享的" + item_type + "干货", 1)
        md.addSimpleLineBreak()
    else:
        file = open(filename, 'a')

    md.addHeader(title, 6)
    if image != "Null":
        md.addImage(image)
    md.addLink(url, url)
    file.write(md.getStream())
    file.close()


def main(wf):
    query = sys.argv[1]
    data = query.split('$')
    if len(data) == 4:
        write_md(data[0], data[1], data[2], data[3])

if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
