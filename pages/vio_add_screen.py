# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: vio_add_screen.py
date: 2019/11/25 16:37
Desc: 三违录入页面元素配置
"""
import allure

from common import read_config
from pages.base_page import BasePage


class VioAddScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\data\\base_xpath.ini")

    vio_date = readeConfigObj.get_config('vioAdd', 'vio_date')
    area_submit_btn = readeConfigObj.get_config('vioAdd', 'area_submit_btn')

    def choose_vio_date(self, vio_date_str):
        with allure.step('选择违章时间：' + vio_date_str):
            self.driver.click_element(self.vio_date)
            self.driver.deal_date_piker(vio_date_str)
            self.driver.click_element(self.area_submit_btn)