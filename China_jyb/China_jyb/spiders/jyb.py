# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
# from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import requests 
from lxml import etree
import re
from China_jyb.items import ChinaJybItem

class JybSpider(RedisSpider):
    name = "jyb"
    allowed_domains = ["jyb.cn"]
    start_urls = (
        'http://china.jyb.cn/',
        # 'http://china.jyb.cn/gnxw/index.html',
    )


    def start_requests(self):
    	reqs = []
        req = Request('http://china.jyb.cn/gnxw/index.html')
        reqs.append(req) 

    	for i in range(1, 10, 1):
    		req = Request('http://china.jyb.cn/gnxw/index_%s.html' % i)
    		reqs.append(req)
    	return reqs

    def collect(self, url, item):
        html = requests.get(url)
        selector = etree.HTML(html.content)
        titles = selector.xpath('//*[@id="body"]/h1/text()')
        for title in titles:
            item['title'] = title
            # print title.encode('utf-8')

        documents = re.findall('<P>(.*?)</P>', html.content, re.S)
        for document in documents:
            content = document.replace('<STRONG>', '').replace('</STRONG>', '').replace('&nbsp;', ' ').replace('<FONT face=仿宋_GB2312', '').replace('color=#0000ff>', '').replace('/FONT', '').replace('<FONT face=仿宋_GB2312>', '').replace('<FONT color=#800000>', '')
            item['content'] = content
            # print content
        return

    def parse(self, response):
        urls = []
        base_url = 'http://china.jyb.cn/gnxw/'
        news_list = response.xpath('//*[@id="sksb"]/div/div/ul[@class="list"]')
        for news in news_list:
            news_urls = news.xpath('li/a/@href').extract()
            for news_url in news_urls:
                url = base_url + news_url.replace('./', '')
                urls.append(url)


        for i in range(len(urls)):
            item = ChinaJybItem()
            self.collect(urls[i], item)
            yield item



