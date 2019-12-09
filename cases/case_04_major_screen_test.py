# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_04_major_screen_test.py
date: 2019/11/27 11:07
Desc: 重大风险清单
"""

import allure
import pytest

from common.init_operate import BaseTest
from common.mysql_operation import ConnMysql
from config import sql_constants
from pages.home_screen import HomeScreen
from pages.major_risk_screen import MajorRiskScreen

conn = ConnMysql()


@allure.feature('重大风险清单')
class TestMajorDanger(BaseTest):

    # hazard_names = conn.get_infos(sql_constants.get_hazard_name_of_danger_sql())
    # hazard_name = hazard_names[random.randint(0, len(hazard_names) - 1)][0]

    hazard_name = '矿井测风工'

    # @pytest.mark.smoketest
    @allure.title('危险源关联风险点')
    @pytest.mark.parametrize('hazard_name', [hazard_name])
    def test_01_risk_points(self, hazard_name):
        """危险源关联风险点"""
        self.home_screen.select_module(HomeScreen.major_risk)
        self.major_screen.click_module(MajorRiskScreen.riskPoint, hazard_name)
        with allure.step('统计危险源关联的风险点'):
            address_list = self.major_screen.collect_risk_point_on_hazard()
        with allure.step('统计数据库中危险源关联的风险点'):
            _address_list_db = conn.get_infos(sql_constants.address_on_hazard_sql(hazard_name))
        address_list_db = []  # 将获取到的数据转化为list
        for item in _address_list_db:
            address_list_db.append(item[0])
        try:
            with allure.step('验证数据'):
                self.driver.assert_equal(address_list, address_list_db)
            self.driver.click_back()  # 点击返回操作，执行之后的操作
        except AssertionError as msg:
            self.driver.click_back()  # 点击返回操作，执行之后的操作
            raise msg

    # @pytest.mark.smoketest
    @allure.title('危险源关联管控措施')
    @pytest.mark.parametrize('hazard_name', [hazard_name])
    def test_02_manage_on_hazard(self, hazard_name):
        # self.home_screen.select_module(HomeScreen.major_risk)
        self.major_screen.click_module(MajorRiskScreen.riskManage, hazard_name)
        with allure.step('统计危险源关联的管控措施'):
            manage_list = self.major_screen.collect_manage_on_hazard()
        with allure.step('统计数据库中危险源关联的管控措施'):
            manage_list_dbs = conn.get_infos(sql_constants.manage_on_hazard_sql(hazard_name))
            manage_list_db = []
            for item in manage_list_dbs:
                manage_list_db.append(item)
        try:
            with allure.step('验证数据'):
                self.driver.assert_equal(manage_list, manage_list_db)
            self.driver.click_back()  # 点击返回操作，执行之后的操作
        except AssertionError as msg:
            self.driver.click_back()  # 点击返回操作，执行之后的操作
            raise msg

    # @pytest.mark.smoketest
    @allure.title('危险源详情')
    @pytest.mark.parametrize('hazard_name', [hazard_name])
    def test_03_detail_of_risk(self, hazard_name):
        # self.home_screen.select_module(HomeScreen.major_risk)
        self.major_screen.click_module(MajorRiskScreen.risk_source_name, hazard_name)
        with allure.step('统计危险源详情：'):
            detail = self.major_screen.collect_detail_of_risk()
            detail_db = self.driver.collect_detail_of_risk(hazard_name)
        try:
            with allure.step('验证数据'):
                self.driver.assert_dict_equal(detail, detail_db)
                # 返回主界面 👇
            self.driver.click_back()
            self.driver.click_back()
        except AssertionError as msg:
            self.driver.click_back()  # 返回主界面 👇
            self.driver.click_back()
            raise msg


