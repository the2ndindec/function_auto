# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_03_vio_add_screen_test.py
date: 2019/11/25 16:41
Desc: 三违录入
"""
import allure
import pytest

from common.init_operate import BaseTest
from pages.home_screen import HomeScreen


class TestVioAdd(BaseTest):

    # @pytest.mark.smoketest
    def test_01_add_vio_success(self):
        """三违数据上报"""
        self.home_screen.select_module(HomeScreen.three_vio_add)
        self.vio_add_screen.choose_vio_date('2019-11-26')
        self.vio_add_screen.choose_vio_address("南翼集中煤仓")
        self.vio_add_screen.choose_vio_people('马勇')
        self.vio_add_screen.choose_vio_level('一般B级')
        self.vio_add_screen.choose_vio_check_unit('综采一区')
        self.vio_add_screen.type_vio_desc('三违事实描述内容')
        self.vio_add_screen.choose_vio_shift('早班')
        self.vio_add_screen.choose_vio_unit('综采二区')
        self.vio_add_screen.choose_vio_category('违规作业')
        self.vio_add_screen.choose_vio_qualitative('一般三违')
        self.vio_add_screen.choose_stop_person('马勇')
        self.driver.swipe_up()
        self.vio_add_screen.submit_vio()
        # 以上为录入三违相关数据 ↑，之后返回主界面，上报三违数据 ↓
        self.driver.click_back()
        self.home_screen.select_module(HomeScreen.vio_upload)
        # todo add assertion

    # @pytest.mark.smoketest
    def test_02_vio_detail(self):
        # 单独执行时需要加上这句 👇
        self.home_screen.select_module(HomeScreen.three_vio_add)
        with allure.step('切换到已上报列表选择三违数据查看详情'):
            self.driver.click_element(self.vio_add_screen.uploaded_tab)
            self.vio_add_screen.choose_and_click_vio('2018-10-22', '南翼集中煤仓', '综采一区', '三违事实12dasd1描ss述a')

        with allure.step('分别通过app和数据库获取三违详情内容'):
            details = self.vio_add_screen.collect_detail_of_vio()
            details_db = self.vio_add_screen.collect_detail_of_vio_from_db('2018-10-22', '南翼集中煤仓', '综采一区', '三违事实12dasd1描ss述a')
        self.driver.assert_dict_equal(details, details_db)
        self.driver.click_back()
        self.driver.click_back()
