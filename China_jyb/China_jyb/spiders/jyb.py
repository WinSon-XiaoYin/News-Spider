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


    def parse(self, response):
        urls = []
        base_url = 'http://china.jyb.cn/gnxw/'
        news_list = response.xpath('//*[@id="sksb"]/div/div/ul[@class="list"]')
        for news in news_list:
            news_urls = news.xpath('li/a/@href').extract()
            for news_url in news_urls:
                url = base_url + news_url.replace('./', '')
                urls.append(url)

        items = []
        for i in range(len(urls)):
            item = ChinaJybItem()
            html = requests.get(urls[i])
            selector = etree.HTML(html.content)
            titles = selector.xpath('//*[@id="body"]/h1/text()')
            for title in titles:
                item['title'] = title
                

            documents = re.findall('<P>(.*?)</P>', html.content, re.S)
            for document in documents:
                item['content'] = document
            items.append(item)
        yield items



