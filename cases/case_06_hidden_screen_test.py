# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_06_hidden_screen_test.py
date: 2019/11/29 10:57
Desc: 隐患录入
"""
import allure
import pytest

from common.init_operate import BaseTest
from pages.home_screen import HomeScreen
from common.excel_operate import read_excel


@allure.feature('隐患录入')
class TestHiddenScreen(BaseTest):

    hidden_params = read_excel('hidden', 2)  # 获取excel文件中参数

    # @pytest.mark.smoketest
    @allure.title('隐患录入')
    @pytest.mark.dependency(name="ahc")
    def test_01_add_hidden(self):
        self.home_screen.select_module(HomeScreen.risk_add)
        with allure.step('录入隐患数据'):
            self.driver.choose_attr_value(self.hidden_screen.exam_type, self.hidden_params['exam_type'])  # 选择检查类型
            self.hidden_screen.choose_vio_date(self.hidden_params['exam_date'])  # 选择检查时间
            self.driver.choose_attr_value(self.hidden_screen.exam_shift, self.hidden_params['exam_shift'])  # 选择班次
            self.driver.choose_attr_value(self.hidden_screen.exam_address, self.hidden_params['address'])  # 选择地点
            # 选择检查人.如果检查类型为‘上级检查’需要手动输入检查人
            if self.hidden_params['exam_type'] == '上级检查':
                self.hidden_screen.type_exam_check_man(self.hidden_params['check_man'])
            else:
                self.driver.choose_attr_value(self.hidden_screen.exam_check_man, self.hidden_params['check_man'])
            self.driver.choose_attr_value(self.hidden_screen.exam_duty_unit, self.hidden_params['duty_unit'])  # 责任单位
            self.driver.choose_attr_value(self.hidden_screen.exam_duty_man, self.hidden_params['duty_man'])  # 责任人
            self.driver.choose_attr_value(self.hidden_screen.exam_hidden_category, self.hidden_params['hidden_category'])  # 隐患类别
            self.driver.choose_attr_value(self.hidden_screen.exam_hidden_level, self.hidden_params['hidden_level'])  # 隐患等级
            self.driver.choose_attr_value(self.hidden_screen.exam_hidden_type, self.hidden_params['hidden_type'])  # 隐患类型
            self.hidden_screen.type_hidden_desc(self.hidden_params['problem_desc'])  # 隐患描述
            self.driver.swipe_up()  # 滑动界面
            # 隐患处理方式
            if self.hidden_params['deal_type'] == 'limit':
                self.hidden_screen.choose_deal_type(type_str='limit', limit_date_str=self.hidden_params['limit_date'])
            else:
                self.hidden_screen.choose_deal_type(type_str='current', review_man_str=self.hidden_params['review_man'])
            self.vio_add_screen.upload_images(2)
        self.driver.click_element(self.hidden_screen.exam_save_btn)  # 保存隐患数据
        try:
            self.driver.assert_true(self.driver.is_toast_exist('提交成功'))
            self.driver.click_back()  # 返回到主页界面
            # self.driver.click_element(self.home_screen.risk_upload)  # 上报隐患数据
        except AssertionError as msg:
            self.driver.click_back()  # 返回到主页界面
            raise msg

    # @pytest.mark.smoketest
    @allure.title('隐患录入--已上报数据查看详情')
    def test_02_add_hidden_detail(self):
        self.home_screen.select_module(HomeScreen.risk_add)  # 单独运行时取消这行的注释 👈
        self.driver.click_element(self.hidden_screen.uploaded_tab)
        _params = self.driver.get_params_of_hidden('1')
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0])
        with allure.step('统计隐患详情信息'):
            detail_app = self.driver.collect_detail_of_hidden()
            detail_db = self.driver.collect_detail_of_hidden_from_db(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0])

        try:
            self.driver.assert_dict_equal(detail_app, detail_db)
            self.driver.click_back()  # 点击两次返回按钮，返回到主页界面
            self.driver.click_back()
        except AssertionError as msg:
            self.driver.click_back()  # 点击两次返回按钮，返回到主页界面
            self.driver.click_back()
            raise msg
