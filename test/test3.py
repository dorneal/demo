#!/usr/bin/python3
# coding:utf-8
# Filename:test3.py
# Author:黄鹏
# Time:2018.04.13 16:03
"""
读取该目录下的所有文件名
"""

import os

import re

path = r"C:\Users\Administrator\Desktop\workspace\day0413\data\\"

# 获取该目录下所有文件，存入列表中
f = os.listdir(path)

for i in f:
    # 设置旧文件名（就是路径+文件名）
    print(i)
    temp = i
    newfilename = temp.split()[1]
    # 匹配数字
    num = re.findall("[0-9]+", newfilename)[0]
    num += '.xml'
    oldname = path + i
    newname = path + num

    # 用os模块中的rename方法对文件改名
    os.rename(oldname, newname)
    print(oldname, '======>', num)
