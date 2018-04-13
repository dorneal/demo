#!/usr/bin/python3
# coding:utf-8
# Filename:test.py
# Author:黄鹏
# Time:2018.04.12 9:08

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

"""
selenium 使用代理，测试
"""

proxy = Proxy(
    {
        'proxyType': ProxyType.MANUAL,
        'httpProxy': '107.172.10.24:1080'  # 代理ip和端口
    }
)
# 新建一个“期望的技能”，哈哈
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# 把代理ip加入到技能中
proxy.add_to_capabilities(desired_capabilities)
driver = webdriver.PhantomJS(
    desired_capabilities=desired_capabilities
)
driver.get('http://httpbin.org/ip')
print(driver.page_source)

# 现在开始切换ip
# 再新建一个ip
proxy = Proxy(
    {
        'proxyType': ProxyType.MANUAL,
        'httpProxy': '202.145.2.53:8080'  # 代理ip和端口
    }
)
# 再新建一个“期望技能”，（）
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# 把代理ip加入到技能中
proxy.add_to_capabilities(desired_capabilities)
# 新建一个会话，并把技能传入
driver.start_session(desired_capabilities)
driver.get('http://httpbin.org/ip')
print(driver.page_source)
driver.close()
