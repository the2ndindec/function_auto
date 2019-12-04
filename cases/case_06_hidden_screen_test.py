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


@allure.feature('隐患录入')
class TestHiddenScreen(BaseTest):

    # @pytest.mark.smoketest
    @allure.title('隐患录入')
    @pytest.mark.dependency(name="ahc")
    def test_01_add_hidden_limit(self):
        self.home_screen.select_module(HomeScreen.risk_add)
        with allure.step('录入隐患数据'):
            self.driver.choose_attr_value(self.hidden_screen.exam_type, '管理干部下井')  # 选择检查类型
            self.hidden_screen.choose_vio_date('2019-12-01')  # 选择检查时间
            self.driver.choose_attr_value(self.hidden_screen.exam_shift, '晚班')  # 选择班次
            self.driver.choose_attr_value(self.hidden_screen.exam_address, '南七回风25度上山')  # 选择地点
            self.driver.choose_attr_value(self.hidden_screen.exam_check_man, '丁德涛')  # 选择检查人
            self.driver.choose_attr_value(self.hidden_screen.exam_duty_unit, '地测科')  # 责任单位
            self.driver.choose_attr_value(self.hidden_screen.exam_duty_man, '刘春东')  # 责任人
            self.driver.choose_attr_value(self.hidden_screen.exam_hidden_category, '保险')  # 隐患类别
            self.driver.choose_attr_value(self.hidden_screen.exam_hidden_level, '一般隐患C级')  # 隐患等级
            self.driver.choose_attr_value(self.hidden_screen.exam_hidden_type, '顶板')  # 隐患类型
            self.hidden_screen.type_hidden_desc('隐患描述1203003')  # 隐患描述
            # self.driver.swipe_up()  # 滑动界面
            self.hidden_screen.choose_deal_type(type_str='limit', limit_date_str='2019-12-02')  # 处理方式
        self.driver.click_element(self.hidden_screen.exam_save_btn)  # 保存隐患数据
        self.driver.assert_true(self.driver.is_toast_exist('提交成功'))
        self.driver.click_back()  # 返回到主页界面
        self.driver.click_element(self.home_screen.risk_upload)  # 上报隐患数据

    # @pytest.mark.smoketest
    @allure.title('隐患录入--已上报数据查看详情')
    def test_02_add_hidden_detail(self):
        self.home_screen.select_module(HomeScreen.risk_add)  # 单独运行时取消这行的注释 👈
        self.driver.click_element(self.hidden_screen.uploaded_tab)
        _params = self.driver.get_paras_of_hidden('1')
        with allure.step('选择隐患数据'):
            self.driver.scroll_and_click_element(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0])
        with allure.step('统计隐患详情信息'):
            detail_app = self.driver.collect_detail_of_hidden()
            detail_db = self.driver.collect_detail_of_hidden_from_db(exam_desc=_params[2], exam_type=_params[1], exam_date=_params[0])
        self.driver.assert_dict_equal(detail_app, detail_db)
        self.driver.click_back()  # 点击两次返回按钮，返回到主界面
        self.driver.click_back()
