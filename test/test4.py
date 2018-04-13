#!/usr/bin/python3
# coding:utf-8
# Filename:test4.py
# Author:黄鹏
# Time:2018.04.13 16:18

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

    all_content = ""
    count = 0
    with open(path + i, "r", encoding="utf-8") as w1:
        for line in w1:
            if i[:-4] in line:
                line = line.replace(i[:-4], num[:-4])
            if 'Difficult' in line:
                line = line.replace('Difficult', 'Difficult'.lower())
            all_content += line
    w1.close()

    # 重新写入内容
    with open(path + i, "w", encoding="utf-8") as w2:
        w2.write(all_content)
        w2.flush()
    w2.close()

    # 用os模块中的rename方法对文件改名
    os.rename(oldname, newname)
