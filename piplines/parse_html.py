#!/usr/bin/python3
# coding:utf-8
# Filename:parse_html.py
# Author:黄鹏
# Time:2018.04.10 11:41

from lxml import etree

"""
    按照携程的城市级联，解析提取存储到本地
"""

f = open("../resource/parse.html", encoding="utf-8")
res = f.read()
tree = etree.HTML(res)
dd = tree.xpath("//dd")
w = open(r"../resource/cities.txt", "a+", encoding="utf-8")
for d in dd:
    a = d.xpath("./a/@data")
    for data in a:
        city = data.split("|")[1]
        w.write(city + "\n")
        print(city)
w.close()
f.close()
