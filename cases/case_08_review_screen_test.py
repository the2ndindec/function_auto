# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_08_review_screen_test.py
date: 2019/12/3 16:29
Desc:
"""
import allure
import pytest

from common.init_operate import BaseTest
from pages.home_screen import HomeScreen


@allure.feature('隐患复查')
class TestReviewScreen(BaseTest):

    # @pytest.mark.smoketest
    @allure.title('隐患复查通过')
    def test_01_review_pass(self):
        self.home_screen.select_module(HomeScreen.risk_review)
        _params = self.driver.get_params_of_hidden()
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0], exam_unit=_params[3])
        self.pending_review_screen.review_pass('2019-12-01', '马勇', '早班', '复查措施1202001')
        try:
            self.driver.assert_true(self.driver.is_toast_exist('提交成功'))
            self.driver.click_back()  # 返回到主页界面
        except AssertionError as msg:
            self.driver.click_back()  # 返回到主页界面
            raise msg

    @allure.title('隐患复查不通过')
    def test_02_review_reject(self):
        # self.home_screen.select_module(HomeScreen.risk_review)  # 单独运行时取消这行的注释 👈
        _params = self.driver.get_params_of_hidden()
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0], exam_unit=_params[3])
        with allure.step('录入相关信息'):
            self.pending_review_screen.review_reject('2019-12-01', '2019-12-01', '马勇', '早班', '复查butongguo措施1202001')
        try:
            self.driver.assert_true(self.driver.is_toast_exist('提交成功'))
            self.driver.click_back()  # 返回到主页界面
        except AssertionError as msg:
            self.driver.click_back()  # 返回到主页界面
            raise msg

    # @pytest.mark.smoketest
    @allure.title('已复查隐患查看详情')
    def test_03_reviewed_detail(self):
        self.home_screen.select_module(HomeScreen.risk_review)  # 单独运行时取消这行的注释 👈
        self.driver.click_element(self.pending_review_screen.reviewed_tab)
        _params = self.driver.get_params_of_hidden()
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0], exam_unit=_params[3])
        with allure.step('统计隐患详情信息'):
            detail_app = self.driver.collect_detail_of_hidden()
            detail_db = self.driver.collect_detail_of_hidden_from_db(_params[0], _params[1], _params[2], check='check:'+_params[3])
        try:
            self.driver.assert_dict_equal(detail_app, detail_db)
            self.driver.click_back()  # 返回到数据列表界面
        except AssertionError as msg:
            self.driver.click_back()  # 返回到数据列表界面
            raise msg

    # @pytest.mark.smoketest
    @allure.title('隐患复查时查看数据详情')
    def test_04_reviewing_detail(self):
        # self.home_screen.select_module(HomeScreen.risk_review)  # 单独运行时取消这行的注释 👈
        self.driver.click_element(self.pending_review_screen.un_review_tab)
        _params = self.driver.get_params_of_hidden()
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0], exam_unit=_params[3])
        self.driver.click_element(self.pending_review_screen.detail_tab)
        with allure.step('统计隐患详情信息'):
            detail_app = self.driver.collect_detail_of_hidden()
            detail_db = self.driver.collect_detail_of_hidden_from_db(_params[0], _params[1], _params[2], check='check:'+_params[3])
        self.driver.assert_dict_equal(detail_app, detail_db)
