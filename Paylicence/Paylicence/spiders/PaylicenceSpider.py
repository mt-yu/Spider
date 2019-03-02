# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from Paylicence.items import PaylicenceItem
import re


class PaylicencespiderSpider(scrapy.Spider):
    name = 'PaylicenceSpider'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://m.sohu.com/a/242659579_712322/?pvid=000115_3w_a'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        try:
            # 爬取数据 保存到scrapy.item中
            item = PaylicenceItem()
            Paylicences = response.xpath('//*[@id="articleContent"]/div/p/strong/parent::*')

            batchs = response.xpath('//*[@id="articleContent"]/div/p').re('第\S批\(\S*\)')
            batch_one = eval(batchs[0][4:-2])
            batch_two = eval(batchs[1][4:-2])
            batch_three = eval(batchs[2][4:-2])
            batch_four = eval(batchs[3][4:-2])
            a = 0
            for pl in Paylicences:
                if pl.xpath('./strong').extract()[0].split()[0][8:].isdigit():
                    item['number'] = pl.xpath('./strong').extract()[0].split()[0][8:]
                    if eval(item['number']) <= batch_one:
                        item['batch'] = '第一批'
                    elif batch_one < eval(item['number']) <= batch_one + batch_two:
                        item['batch'] = '第二批'
                    elif batch_one + batch_two < eval(item['number']) <= batch_one + batch_two + batch_three:
                        item['batch'] = '第三批'
                    elif batch_one + batch_two + batch_three < eval(
                            item['number']) <= batch_one + batch_two + batch_three + batch_four:
                        item['batch'] = '第四批'
                    else:
                        item['batch'] = '第五批'
                    item['name'] = pl.xpath('./strong').extract()[0].split()[1].split('</strong>')[0]
                    item['licensing_time'] = pl.xpath('./text()').extract()[0].split()[0]
                    item['business_area'] = pl.xpath('./text()').extract()[0].split()[1]
                    yield item
                else:
                    a += 1
                    print('-------------------{}--------------'.format(a))
                    print('-------------------{}--------------'.format(len(Paylicences)))

        except Exception as e:
            print('error:---------------------{}--------------------'.format(e))
