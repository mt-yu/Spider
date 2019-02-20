# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapyspider2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AirasiaItem(scrapy.Item):
    price = scrapy.Field()  # 价格
    departure = scrapy.Field()  # 出发地
    destination = scrapy.Field()  # 目的地
    time = scrapy.Field()  # 时间段
    date = scrapy.Field()  # 日期字段
