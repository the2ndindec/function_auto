# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: home_screen.py
date: 2019/11/25 14:33
Desc: 首页元素配置
"""
from common import read_config
from pages.base_page import BasePage


class HomeScreen(BasePage):

    read_ConfigObj = read_config.ReadConfig("\\data\\base_xpath.ini")

    # 重大风险清单
    major_risk = read_ConfigObj.get_config('home', 'major_risk')
    # 风险点
    address_point = read_ConfigObj.get_config('home', 'risk_point')
    # 三违录入
    three_vio_add = read_ConfigObj.get_config('home', 'three_vio_add')
    # 三违查询
    three_vio_search = read_ConfigObj.get_config('home', 'three_vio_search')
    # 隐患录入
    risk_add = read_ConfigObj.get_config('home', 'risk_add')
    # 隐患整改
    risk_reform = read_ConfigObj.get_config('home', 'risk_reform')
    # 隐患复查
    risk_review = read_ConfigObj.get_config('home', 'risk_review')
    # 超期隐患
    risk_delay = read_ConfigObj.get_config('home', 'risk_delay')
    # 隐患数据上报
    risk_upload = read_ConfigObj.get_config('home', 'risk_upload')
    # 三违数据上报
    vio_upload = read_ConfigObj.get_config('home', 'vio_upload')
    # 同步数据
    synchronize = read_ConfigObj.get_config('home', 'synchronize')
    synchronize_submit = read_ConfigObj.get_config('home', 'synchronize_confirm')

    def sync_data(self):
        """同步数据"""
        self.driver.click_element(self.synchronize)
        self.driver.click_element(self.synchronize_submit)

    def select_module(self, loc):
        self.driver.click_element(loc)

    def get_toast(self, toast):
        """获取toast"""
        self.driver.is_toast_exist(toast)
