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

from common.excel_operate import read_excel
from common.init_operate import BaseTest
from pages.home_screen import HomeScreen


class TestVioAdd(BaseTest):

    @pytest.mark.smoketest
    def test_01_add_vio_success(self):
        """三违数据上报"""
        self.vio_params = read_excel('vio', 2)  # 获取excel文件中参数
        self.home_screen.select_module(HomeScreen.three_vio_add)
        with allure.step('录入三违数据：'):
            self.vio_add_screen.choose_vio_date(self.vio_params['vio_date'])
            self.vio_add_screen.choose_vio_address(self.vio_params['vio_address'])
            self.vio_add_screen.choose_vio_people(self.vio_params['vio_people'])
            self.vio_add_screen.choose_vio_level(self.vio_params['vio_level'])
            self.vio_add_screen.choose_vio_check_unit(self.vio_params['vio_check_unit'])
            self.vio_add_screen.type_vio_desc(self.vio_params['vio_desc'])
            self.vio_add_screen.choose_vio_shift(self.vio_params['vio_shift'])
            self.vio_add_screen.choose_vio_unit(self.vio_params['vio_unit'])
            self.vio_add_screen.choose_vio_category(self.vio_params['vio_category'])
            self.vio_add_screen.choose_vio_qualitative(self.vio_params['vio_qualitative'])
            self.vio_add_screen.choose_stop_person(self.vio_params['stop_person'])
            self.driver.swipe_up()
            self.vio_add_screen.upload_images(3)
            self.vio_add_screen.submit_vio()
        try:
            self.driver.assert_true(self.driver.is_toast_exist('数据已经保存本地'))
            # 以上为录入三违相关数据 ↑，之后返回主界面，上报三违数据 ↓
            self.driver.click_back()
            # self.home_screen.select_module(HomeScreen.vio_upload)  # 上报三违数据
        except AssertionError as msg:
            self.driver.click_back()
            raise msg

    # @pytest.mark.smoketest
    def test_02_vio_detail(self):
        # 单独执行时需要加上这句 👇
        self.home_screen.select_module(HomeScreen.three_vio_add)
        with allure.step('切换到已上报列表选择三违数据查看详情'):
            self.driver.click_element(self.vio_add_screen.uploaded_tab)
        with allure.step('选择三违数据'):
            _param = self.vio_add_screen.get_vio_params()
            self.vio_add_screen.choose_and_click_vio(_param[0], _param[1], _param[2], _param[3])
        with allure.step('分别通过app和数据库获取三违详情内容'):
            details = self.vio_add_screen.collect_detail_of_vio()
            details_db = self.vio_add_screen.collect_detail_of_vio_from_db(_param[0], _param[1], _param[2], _param[3])
        try:
            self.driver.assert_dict_equal(details, details_db)
            self.driver.click_back()  # 两次返回操作，返回到主页界面
            self.driver.click_back()
        except AssertionError as msg:
            self.driver.click_back()  # 两次返回操作，返回到主页界面
            self.driver.click_back()
            raise msg
