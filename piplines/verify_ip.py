#!/usr/bin/python3
# coding:utf-8
# Filename:verify_ip.py
# Author:黄鹏
# Time:2018.04.12 17:44
import threading

import requests


def t1():
    # ip代理池
    proxy_ip_pool = []
    ip_msg = open(r"../resource/available_ip.txt", encoding="utf-8")
    for line in ip_msg:
        address = line.strip()
        proxy_ip_pool.append(address)
    ip_msg.close()

    url = "http://flights.ctrip.com"
    w = open("../resource/ctrip_ip1.txt", "a+", encoding="utf-8")
    for proxy_ip in proxy_ip_pool:
        try:
            requests.get(url=url, timeout=30, proxies={"http": proxy_ip})
        except:
            print("T1 这个{0}不行".format(proxy_ip))
            continue
        else:
            w.write(proxy_ip + "\n")
            w.flush()
    w.close()


def t2():
    # ip代理池
    proxy_ip_pool = []
    ip_msg = open(r"../resource/proxy_ip2.txt", encoding="utf-8")
    for line in ip_msg:
        address = line.strip()
        proxy_ip_pool.append(address)
    ip_msg.close()

    url = "http://flights.ctrip.com"
    w = open("../resource/ctrip_ip2.txt", "a+", encoding="utf-8")
    for proxy_ip in proxy_ip_pool:
        try:
            requests.get(url=url, timeout=30, proxies={"http": proxy_ip})
        except:
            print("T2 这个{0}不行".format(proxy_ip))
            continue
        else:
            w.write(proxy_ip + "\n")
            w.flush()
    w.close()


def t3():
    # ip代理池
    proxy_ip_pool = []
    ip_msg = open(r"../resource/total_ip_pool.txt", encoding="utf-8")
    for line in ip_msg:
        address = line.strip()
        proxy_ip_pool.append(address)
    ip_msg.close()

    url = "http://flights.ctrip.com"
    w = open("../resource/ctrip_ip3.txt", "a+", encoding="utf-8")
    for proxy_ip in proxy_ip_pool:
        try:
            requests.get(url=url, timeout=30, proxies={"http": proxy_ip})
        except:
            print("T3 这个{0}不行".format(proxy_ip))
            continue
        else:
            w.write(proxy_ip + "\n")
            w.flush()
    w.close()


if __name__ == "__main__":
    t1 = threading.Thread(target=t1)
    t2 = threading.Thread(target=t2)
    t3 = threading.Thread(target=t3)
    t1.start(), t2.start(), t3.start()
    t1.join(), t2.join(), t3.join()
