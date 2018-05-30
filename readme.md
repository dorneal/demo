## 爬取携程机票信息（程序性能取决于`代理池`的质量）
### 本程序提供三种方案
+ 使用自带的爬虫网络库（完善待优化）
+ 使用requests（完善待优化）

### 本程序调用了以下第三方库
+ requests
+ BeautifulSoup4
+ lxml

### 目录说明：
+ handler
    - requests_spider.py:主程序1
    - urllib_spider.py:主程序2
+ parse
    - parse_html.py : 从HTML中，解析全国的城市列表及编号并存入到cities.txt文本中
    - parse_ip.py : 解析代理IP文本（total_ip_pool.txt）中可用的代理IP，并存入到ctrip_ip3.txt文本中，便于爬虫主程序调用
+ resource
    - ban_ip.txt 从主程序中使用过的代理ip失效后，保存到ban_ip.txt
    - cities.txt 城市及编号列表
    - ctrip_ip3.txt 主要使用的IP代理池
    - OceanBall.js 携程反爬js片段，用于分析如何解密参数
    - parse.html 城市及编号HTML片段
    - results1.txt 爬取后的结果保存文本
    - total_ip_pool.txt 在免费代理IP网站爬取到的免费代理IP文本
    
## 使用：
- 修改源码，更改日期，直接启用requests_spider主程序即可，结果保存在/resource/results1.txt中
- 修改源码，更改日期，直接启用urllib_spider主程序即可，结果将会自动生成一个results2.txt文本中