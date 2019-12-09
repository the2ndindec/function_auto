# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: pending_rectify_screen.py
date: 2019/12/2 15:53
Desc: 隐患整改
"""
import allure

from common import read_config
from pages.base_page import BasePage


class PendingRectifyScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\config\\base_xpath.ini")
    rectified_tab = readeConfigObj.get_config('rectify', 'rectified_tab')  # 已整改
    un_rectify_tab = readeConfigObj.get_config('rectify', 'un_rectify_tab')  # 待整改
    rectifing_tab = readeConfigObj.get_config('rectify', 'rectifing_tab')  # 通过·不通过
    detail_tab = readeConfigObj.get_config('rectify', 'detail_tab')  # 详细信息
    pass_radio = readeConfigObj.get_config('rectify', 'pass_radio')  # 通过
    unPass_radio = readeConfigObj.get_config('rectify', 'unPass_radio')  # 不通过
    modifyDate = readeConfigObj.get_config('rectify', 'modifyDate')  # 整改时间
    modifyMan = readeConfigObj.get_config('rectify', 'modifyMan')  # 整改人
    modifyShift = readeConfigObj.get_config('rectify', 'modifyShift')  # 整改班次
    rectMeasures = readeConfigObj.get_config('rectify', 'rectMeasures')  # 整改措施
    rectMeasures_area = readeConfigObj.get_config('rectify', 'rectMeasures_area')  # 输入框
    submit_btn_area = readeConfigObj.get_config('rectify', 'submit_btn_area')  # 输入框界面提交按钮
    descOfReject = readeConfigObj.get_config('rectify', 'descOfReject')  # 驳回备注
    submit_pass_btn = readeConfigObj.get_config('rectify', 'submit_pass_btn')  # 通过界面提交按钮
    submit_unPass_btn = readeConfigObj.get_config('rectify', 'submit_unPass_btn')  # 驳回界面提交按钮
    toast_tips = readeConfigObj.get_config('rectify', 'toast_tips')  # toast提示信息

    def rectify_pass(self, modify_date_str, modify_man_str, modify_shift_str, rect_measures_str):
        """
        隐患整改通过
        :param modify_date_str: 整改时间
        :param modify_man_str: 整改人
        :param modify_shift_str: 整改班次
        :param rect_measures_str: 整改措施
        :return:
        """
        with allure.step('选择整改时间:' + modify_date_str):
            self.driver.click_element(self.modifyDate)
            self.driver.deal_date_piker(modify_date_str)
            self.driver.click_element(self.submit_btn_area)
        with allure.step('选择整改人：' + modify_man_str):
            self.driver.choose_attr_value(self.modifyMan, modify_man_str)
        with allure.step('选择整改班次：' + modify_shift_str):
            self.driver.choose_attr_value(self.modifyShift, modify_shift_str)
        with allure.step('录入整改错误内容：' + rect_measures_str):
            self.driver.click_element(self.rectMeasures)
            self.driver.input_text(self.rectMeasures_area, rect_measures_str)
            self.driver.click_element(self.submit_btn_area)
        with allure.step('提交数据'):
            self.driver.click_element(self.submit_pass_btn)

    def rectify_un_pass(self, reject_str):
        """
        整改不通过
        :param reject_str: 驳回备注内容
        :return:
        """
        with allure.step('录入驳回备注内容:' + reject_str):
            self.driver.click_element(self.unPass_radio)
            self.driver.click_element(self.descOfReject)
            self.driver.input_text(self.rectMeasures_area, reject_str)
            self.driver.click_element(self.submit_btn_area)
        with allure.step('提交数据'):
            self.driver.click_element(self.submit_unPass_btn)
