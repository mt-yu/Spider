# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Request
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from scrapyspider2.items import AirasiaItem


class AirasiaSpider(scrapy.Spider):
    name = 'airasia'

    def __init__(self):
        super(AirasiaSpider, self).__init__()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)  # 全局等待加载时常为30s

    def start_requests(self):
        url = 'https://www.airasia.com/booking/select/zh/cn/HKG/BDO/2019-03-20/N/1/0/0/O/N/HKD/SC'
        yield Request(url)

    def parse(self, response):
        try:
            self.driver.get(response.url)   # 设置浏览器对象
            self.driver.maximize_window()  # 窗口最大化
        except TimeoutException:
            print('Time out')

        try:
            # 展开获得完整的网页显示
            btn1 = self.driver.find_element_by_id('airasia-fares-div-low-fare-selected-0-0-heatmap')
            btn1.click()
            btn2 = self.driver.find_element_by_id('airasia-flight-schedule-div-show-more-flights-button-0-heatmap')
            btn2.click()
        except NoSuchElementException:
            print('No Element')
        finally:
            # 获取js加载后的网页content
            content = self.driver.page_source.encode('utf-8')
            response = HtmlResponse(response.url, encoding='utf-8', body=content, request=Request(response.url))

        try:
            # 爬取数据 保存到scrapy.item中
            item = AirasiaItem()
            item['date'] = response.xpath('//*[@id="airasia-fare-calendar-div-calendar-date-0-19-heatmap"]'
                                          '/div/div[1]/label/text()').extract()[0]
            airasias = response.xpath('//*[@class="row flight-schedule"]')
            for airasia in airasias:
                item['time'] = airasia.xpath('.//*[@id="div-sub-flight-info"]/span/text()').extract()[0]
                item['price'] = airasia.xpath('.//*[@id="amount-desc"]/text()').extract()[0].replace(',', '')
                item['departure'] = airasia.xpath('.//*[@id="fares-depart-desc"]/text()').extract()[0].split()[0]
                item['destination'] = airasia.xpath('.//*[@id="fares-depart-desc"]/text()').extract()[0].split()[2]
                yield item
        except Exception as e:
            print('error:---------------------{}--------------------'.format(e))

        try:
            # 选择最优价格
            select_price_click = self.driver.find_element_by_xpath('//*[@id="airasia-fares-div-fare-to-hover-0-0-heatmap"]')
            select_price_click.click()
            time.sleep(0.5)
            # 选择航班继续按钮
            next_btn1 = self.driver.find_element_by_xpath('//*[@id="select-bottom-booking-summary-airasia-button-inner-button-booking-summary-heatmap"]')
            next_btn1.click()
            time.sleep(0.5)
            # 增值服务继续按钮
            next_btn2 = self.driver.find_element_by_xpath('//*[@id="addons-bottom-booking-summary-airasia-button-inner-button-booking-summary-heatmap"]')
            next_btn2.click()
            # 乘客信息表单填写
            first_name = self.driver.find_element_by_xpath('//*[@id="adult-0-given-name-heatmap-autocomplete-heatmap"]')
            first_name.send_keys('jc')
            last_name = self.driver.find_element_by_xpath('//*[@id="adult-0-sur-name-heatmap"]')
            last_name.send_keys('y')

            # 日期输入

            # body_date = self.driver.find_element_by_xpath('//*[@id="adult-0-dob-heatmap"]').click()
            body_date = self.driver.find_element_by_xpath('/html/body/app-root/div/main/airasia-passenger/content/section/div/guest-details/div/div/guest-adult/div/form/div/div/div[2]/div[2]/airasia-datepicker/form/mat-form-field/div/div[1]/div[2]/mat-datepicker-toggle/button').click()
            year = self.driver.find_element_by_xpath('//*[@id="mat-datepicker-0"]/div/mat-multi-year-view/table/tbody/tr[6]/td[3]/div').click()
            month = self.driver.find_element_by_xpath('//*[@id="mat-datepicker-0"]/div/mat-year-view/table/tbody/tr[4]/td[1]/div').click()
            day = self.driver.find_element_by_xpath('//*[@id="mat-datepicker-0"]/div/mat-month-view/table/tbody/tr[5]/td[1]/div').click()
            # body_date.send_keys('1990/9/24')
            time.sleep(1)
            # 乘客界面继续按钮
            next_btn3 = self.driver.find_element_by_xpath('//*[@id="bottom-booking-summary-airasia-button-inner-button-booking-summary-heatmap"]')
            next_btn3.click()
            time.sleep(5)
        except NoSuchElementException:
            print('No Element')

        finally:
            # 爬取完毕关闭浏览器
            self.driver.close()