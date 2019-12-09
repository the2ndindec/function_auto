# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_05_address_screen_test.py
date: 2019/11/28 13:56
Desc: 风险点模块相关
"""

import allure
import pytest

from common.init_operate import BaseTest
from common.mysql_operation import ConnMysql
from config import sql_constants
from pages.home_screen import HomeScreen
from pages.address_screen import AddressScreen

conn = ConnMysql()


@allure.feature('风险点管理')
class TestAddress(BaseTest):

    # @pytest.mark.smoketest
    @allure.title('风险点关联危险源')
    @pytest.mark.parametrize('address', ['3下905里工作面'])
    def test_01_hazard_on_address(self, address):
        with allure.step('进入风险点管理界面'):
            self.home_screen.select_module(HomeScreen.address_point)
        with allure.step('点击-%s-,查看关联的危险源' % address):
            self.address_point_screen.click_module(AddressScreen.hazard_on_address, address)
        with allure.step('统计危险源数据'):
            hazard = self.address_point_screen.collect_hazard_or_depart_on_address()
            hazard_db = []
            for item in conn.get_infos(sql_constants.hazard_on_address(address)):
                hazard_db.append(item[0])
        try:
            self.driver.assert_equal(hazard, hazard_db)
            self.driver.click_back()  # 👈点击返回操作，执行之后的操作
        except AssertionError as msg:
            self.driver.click_back()  # 👈点击返回操作，执行之后的操作
            raise msg

    # @pytest.mark.smoketest
    @allure.title('风险点关联风险')
    @pytest.mark.parametrize('address', ['3下905里工作面'])
    def test_02_risk_on_address(self, address):
        with allure.step('点击-%s-,查看关联的风险' % address):
            self.address_point_screen.click_module(AddressScreen.risk_on_address, address)
        with allure.step('统计风险点数据'):
            risk = self.address_point_screen.collect_risk_on_address()
            risk_db = []
            for items in conn.get_infos(sql_constants.risk_on_address(address)):
                for item in items:
                    risk_db.append(item)
        try:
            self.driver.assert_equal(risk, risk_db)
            self.driver.click_back()  # 👈点击返回操作，执行之后的操作
        except AssertionError as msg:
            self.driver.click_back()
            raise msg

    # @pytest.mark.smoketest
    @pytest.mark.parametrize('address', ['3下905里工作面'])
    @allure.title('风险点关联责任部门')
    def test_03_depart_on_address(self, address):
        with allure.step('点击-%s-,查看关联的责任部门' % address):
            self.address_point_screen.click_module(AddressScreen.depart_on_address, address)
        with allure.step('统计责任部门数据'):
            depart = self.address_point_screen.collect_hazard_or_depart_on_address()
            depart_db = []
            for item in conn.get_infos(sql_constants.depart_on_address(address)):
                depart_db.append(item[0])
        try:
            self.driver.assert_equal(depart, depart_db)
            self.driver.click_back()  # 👈点击返回操作，执行之后的操作
            self.driver.click_back()
        except AssertionError as msg:
            self.driver.click_back()  # 👈点击返回操作，执行之后的操作
            self.driver.click_back()
            raise msg
