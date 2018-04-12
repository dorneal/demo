#!/usr/bin/python3
# coding:utf-8
# Filename:parse_ip.py
# Author:黄鹏
# Time:2018.04.12 14:31

f = open("../resource/proxy_ip.txt", encoding="utf-8")
w = open("../resource/proxy_ip2.txt", "a+", encoding="utf-8")

for line in f:
    lis = line.strip().split()
    w.write(lis[0] + ":" + lis[1] + "\n")
    w.flush()

f.close()
w.close()
