# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaylicenceItem(scrapy.Item):
    number = scrapy.Field()  # 总序号
    batch = scrapy.Field()  # 批次
    name = scrapy.Field()  # 名称
    licensing_time = scrapy.Field()  # 发牌时间
    business_area = scrapy.Field()  # 业务范围
