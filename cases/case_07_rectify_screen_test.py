# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_07_rectify_screen_test.py
date: 2019/12/2 16:35
Desc: 隐患整改模块脚本
"""
import allure
import pytest

from common.init_operate import BaseTest
from pages.home_screen import HomeScreen


@allure.feature('隐患整改')
class TestRectifyScreen(BaseTest):

    # @pytest.mark.smoketest
    @allure.title('隐患整改通过')
    def test_01_rectify_pass(self):
        self.home_screen.select_module(HomeScreen.risk_reform)
        _params = self.driver.get_params_of_hidden()
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0], exam_unit=_params[3])
        self.pending_rectify_screen.rectify_pass('2019-12-01', '马勇', '早班', '整改措施1202001')
        self.driver.assert_true(self.driver.is_toast_exist('提交成功..'))
        # self.driver.click_back()  # 退回到数据列表界面

    @allure.title('隐患整改查看详情')
    # @pytest.mark.smoketest
    def test_02_detail_on_rectify(self):
        self.home_screen.select_module(HomeScreen.risk_reform)  # 单独运行时取消这行的注释 👈
        _params = self.driver.get_params_of_hidden()
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0], exam_unit=_params[3])
        self.driver.click_element(self.pending_rectify_screen.detail_tab)
        detail_app = self.driver.collect_detail_of_hidden()
        detail_db = self.driver.collect_detail_of_hidden_from_db(_params[0], _params[1], _params[2], depart='depart:'+_params[3])
        try:
            self.driver.assert_dict_equal(detail_app, detail_db)
            self.driver.click_back()  # 退回到数据列表界面
        except AssertionError as msg:
            self.driver.click_back()  # 退回到数据列表界面
            raise msg

    @allure.title('隐患驳回')
    # @pytest.mark.smoketest
    def test_03_rectify_un_pass(self):
        # self.home_screen.select_module(HomeScreen.risk_reform)  # 单独运行时取消这行的注释 👈
        _params = self.driver.get_params_of_hidden()
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0], exam_unit=_params[3])
        self.pending_rectify_screen.rectify_un_pass('测试数据：审核驳回')
        self.driver.assert_true(self.driver.is_toast_exist('驳回成功..'))

    @allure.title('已整改隐患查看详情')
    # @pytest.mark.smoketest
    def test_04_rectified_detail(self):
        # self.home_screen.select_module(HomeScreen.risk_reform)  # 单独运行时取消这行的注释 👈
        self.driver.click_element(self.pending_rectify_screen.rectified_tab)
        _params = self.driver.get_params_of_hidden()
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0], exam_unit=_params[3])
        with allure.step('统计隐患详情信息'):
            detail_app = self.driver.collect_detail_of_hidden()
            detail_db = self.driver.collect_detail_of_hidden_from_db(_params[0], _params[1], _params[2], depart='depart:'+_params[3])
        try:
            self.driver.assert_dict_equal(detail_app, detail_db)
            self.driver.click_back()  # 退回到数据列表界面
            self.driver.click_back()  # 退回到主页界面
        except AssertionError as msg:
            self.driver.click_back()  # 退回到数据列表界面
            self.driver.click_back()  # 退回到主页界面
            raise msg
