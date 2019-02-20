# -*- coding: utf-8 -*-
import scrapy


class WoodenrobotSpider(scrapy.Spider):
    name = 'woodenrobot'    # 爬虫名字 唯一
    allowed_domains = ['woodenrobot.me']    # 网站域
    start_urls = ['http://woodenrobot.me/']  # 第一个开始爬去的url

    def parse(self, response):
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            print(title.strip())
