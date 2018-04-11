#!/usr/bin/python3
# coding:utf-8
# Filename:demo5.py
# Author:黄鹏
# Time:2018.04.10 12:19
import time
from selenium import webdriver
from lxml import etree
from selenium.common.exceptions import TimeoutException

"""
    使用selenium 爬取携程航班信息
    缺点：速度慢，解析需要等待js渲染，难分析提取想要的数据
    优点：不需要抓包信息，简单
"""
driver = webdriver.Chrome()
url = "http://flights.ctrip.com/booking/WUH-SZX---D-adu-1/?ddate1=2018-04-11&ddate2=2018-05-11"

# 设置超时时间
driver.set_page_load_timeout(30)
try:
    driver.get(url)
except TimeoutException:
    # 超过设定时间，停止加载
    driver.execute_script('window.stop()')

# 获取城市输入，日期输入框
# driver.find_element_by_xpath("//*[@id='radio_D']").click()
start_city_input = driver.find_element_by_xpath("//*[@id='DCityName1']")
arrivals_city_input = driver.find_element_by_xpath("//*[@id='ACityName1']")
start_date_input = driver.find_element_by_xpath("//*[@id='DDate1']")
return_date_input = driver.find_element_by_xpath("//*[@id='ReturnDate1']")

# 从文本中读取城市信息
f2 = open(r"C:\Users\Administrator\Desktop\workspace\day0410\cities.txt", encoding="utf-8")
city_list = []
while True:
    city = f2.readline().strip()
    if not city:
        break
    city_list.append(city)

# 将输入框清空
start_city_input.clear()
arrivals_city_input.clear()
start_date_input.clear()
return_date_input.clear()

# 填写输入框信息
start_city_input.send_keys(city_list[0])
arrivals_city_input.send_keys(city_list[1])
start_date_input.send_keys("2018-04-11")
return_date_input.send_keys("2018-05-11")

# 等待一秒，提交
time.sleep(1)
driver.find_element_by_xpath("//*[@id='btnReSearch']").click()

# 等待三秒，获取所有搜索信息
time.sleep(3)
div_list = driver.find_element_by_xpath("//*[@id='J_flightlist2']/div")

# 进行解析，提取需要的信息
div_parse_list = etree.HTML(div_list)

# TODO 存在解析问题，待解决
for div in div_parse_list:
    start_time = div.xpath("./div[2]/div[2]/div[1]/strong/text()").strip()
    arrivals_time = div.xpath("./div[2]/div[4]/div[1]/strong/text()").strip()
    ticks_price = div.xpath("./div[2]/div[8]/span/text()").strip()
    print(start_time + "----" + arrivals_time)
    print(ticks_price)
