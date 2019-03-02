# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
import xlwt
import pandas as pd


class PaylicencePipeline(object):
    def process_item(self, item, spider):
        return item


class Pipeline_ToCSV(object):
    # 参考 https://blog.csdn.net/sc_lilei/article/details/79590696
    def __init__(self):
        # csv文件的位置，无需事先创建
        self.store_file = os.path.dirname(__file__) + '\\spiders\\test.csv'
        # 打开（创建）文件  加入newline 是为了不让每行多出一个空行
        self.file = open(self.store_file, 'w', encoding='utf-8', newline='')
        # csv写入
        self.writer = csv.writer(self.file)
        # 写入表头
        self.writer.writerow(('序号', '批次', '名称', '发牌时间', '业务范围'))

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        if item['number']:
            self.writer.writerow((item['number'], item['batch'], item['name'],
                                  item['licensing_time'],
                                  item['business_area']))
        return item

    def close_spider(self, spider):
        # 关闭爬虫时鼠标将文件保存退出
        self.file.close()
        # 将CSV 文件转换成xlsx 文件保存 使用pandas 模块
        # 参考 https://blog.csdn.net/qq_33689414/article/details/78307031
        csv_to_excel = pd.read_csv(self.store_file, encoding='utf-8')
        # 解决左边多一列的问题 https://blog.csdn.net/guotong1988/article/details/80513879
        csv_to_excel.to_excel('pands_test.xlsx', sheet_name='2018中国第三方支付牌照250家公司名单最新完整版',
                              index=False)

        with open(self.store_file, 'r', encoding='utf-8') as f:
            read = csv.reader(f)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('2018中国第三方支付牌照250家公司名单最新完整版')  # 创建一个sheet表格
            # 设置列宽 参考https://www.cnblogs.com/landhu/p/4978705.html
            sheet.col(0).width = 256 * 6  # xlwt中是行和列都是从0开始计算的
            sheet.col(1).width = 256 * 7
            sheet.col(2).width = 256 * 40
            sheet.col(3).width = 256 * 15
            sheet.col(4).width = 256 * 123
            l = 0
            for line in read:
                print(line)
                r = 0
                for i in line:
                    print(i)
                    sheet.write(l, r, i)  # 一个一个将单元格数据写入
                    r = r + 1
                l = l + 1
            workbook.save('2018中国第三方支付牌照250家公司名单最新完整版.xls')  # 保存Excel
