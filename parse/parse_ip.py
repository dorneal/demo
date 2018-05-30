#!/usr/bin/python3
# coding:utf-8
# Filename:parse_ip.py
# Author:黄鹏
# Time:2018.04.10 15:51
import telnetlib

"""
ip验证提取
从总IP文本中，提取可用的IP，写入到新文本
"""
f = open("../resource/total_ip_pool.txt", encoding="utf-8")
w = open("../resource/available_ip.txt", "a+", encoding="utf-8")
good_ip = []
for l in f:
    line = l.strip()
    ip = line.split(":")[0]
    port = line.split(":")[1]
    # 检测代理ip是否可用
    try:
        telnetlib.Telnet(ip, port=port, timeout=10)
    except:
        print('connect failed')
    else:
        # 保存到项目本地
        w.write(line + "\n")
        w.flush()
        good_ip.append(line)
        print('success')
w.close()
f.close()
print(good_ip)
