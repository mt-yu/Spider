#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
import requests
import json
import jsonpath  # json 的解析器 类似xpath
import csv

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QDoubleSpinBox, QGridLayout, QApplication, QPushButton


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # 将货币Code清单导入
        self.currency = {}
        with open('physical_currency_list.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.currency[row['currency code']] = row['currency name']

        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(self.currency)
        self.fromComboBox.setCurrentText('HKD')  # 设置初始
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(1.00, 10000000.00)
        self.fromSpinBox.setValue(1.00)  # 设置初始
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(self.currency)
        self.toComboBox.setCurrentText('CNY')  # 设置初始
        self.toLabel = QLabel("1.00")  # 设置初始

        self.exchangeButton = QPushButton()
        # self.exchangeButton.setFlat(True)
        # self.exchangeButton.setDefault(True)
        self.exchangeButton.setText('form<==>to互换')

        #  初始显示汇率
        date, rate = self.getdata()
        self.rate = rate
        dateLabel = QLabel(date)
        self.toLabel.setText('{:.3f}'.format(self.rate))  #

        #  格点布局
        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        grid.addWidget(self.exchangeButton, 3, 0)
        self.setLayout(grid)

        # self.connect(self.fromComboBox,
        #         SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.fromComboBox.currentIndexChanged.connect(self.update)

        # self.connect(self.toComboBox,
        #         SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.toComboBox.currentIndexChanged.connect(self.update)

        # self.connect(self.fromSpinBox,
        #         SIGNAL("valueChanged(double)"), self.updateUi)
        self.fromSpinBox.valueChanged.connect(self.updateUi)

        self.exchangeButton.clicked.connect(self.on_exchangeButton_connect_clicked)

        self.fromSpinBox.setFocus()
        self.setWindowTitle("Currency")

    @pyqtSlot()
    def on_exchangeButton_connect_clicked(self):
        flag = self.fromComboBox.currentText()
        self.fromComboBox.setCurrentText(self.toComboBox.currentText())
        self.toComboBox.setCurrentText(flag)

    def update(self):
        _, rate = self.getdata()
        self.rate = rate
        self.updateUi()

    def updateUi(self):
            self.toLabel.setText('{:.3f}'.format(self.rate * self.fromSpinBox.value()))

    def getdata(self):  # Idea taken from the Python Cookbook
        try:
            date = "Unknown"
            api_key = '4CLM7PPORFOSVDZO'

            from_currency = self.fromComboBox.currentText()
            to_currency = self.toComboBox.currentText()

            url = 'https://www.alphavantage.co/query?' \
                  'function=CURRENCY_EXCHANGE_RATE&from_currency=' + from_currency + \
                  '&to_currency=' + to_currency +  \
                  '&apikey=' + api_key

            header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"}

            r = requests.get(url, header)

            data = r.text  # 读取为str 类型
            json_data = json.loads(data)  # 将json格式obj 转换为python dict

            # 获取最后更新的时间
            date = jsonpath.jsonpath(json_data, "$..*")[-2]  # 1. *** 这种格式的Json key 不知道要怎么解析查找

            # 将汇率保存到 rate
            rate = jsonpath.jsonpath(json_data, "$..*")[-3]
            rate = eval(rate)
            return "Exchange Rates Date: " + date, rate
        except Exception as e:
            return "Failed to download:\n{}".format(e)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

