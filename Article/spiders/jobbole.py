# -*- coding: utf-8 -*-
import re

import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112706/']

    def parse(self, response):
        re_selector = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1")
        re2_selector = response.xpath('//*[@id="post-112706"]/div[1]/h1/text()')
        re3_selector = response.xpath('//*[@id="post-112706"]/div[2]/p/text()')
        re4_selector = response.xpath('//*[@id="post-112706"]/div[3]/div[3]/span[2]/text()').extract()[0]
        print(re3_selector.extract()[0].replace("·","").strip())#extract()去除路径元素,[0]为第一位内容,strip()去除换行空格
        print(re3_selector.extract())
        print(re2_selector.extract())
        print(re2_selector)
        print(re4_selector)
        matchbox = re.match(".*?((\d.+\d).|\d{1}).*", re4_selector)
        if matchbox:
            print(matchbox.group(1))
        pass
