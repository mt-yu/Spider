# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 类似与ORM
    pass



class DoubanMovieItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()

    #分别对应的xpath路径
    # // *[ @ id = "content"] / div / div[1] / ol / li[1] / div / div[1] / em
    # // *[ @ id = "content"] / div / div[1] / ol / li[1] / div / div[2] / div[1] / a / span[1]
    # // *[ @ id = "content"] / div / div[1] / ol / li[1] / div / div[2] / div[2] / div / span[2]
    # // *[ @ id = "content"] / div / div[1] / ol / li[1] / div / div[2] / div[2] / div / span[4]


