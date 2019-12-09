# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: pending_review_screen.py
date: 2019/12/2 15:54
Desc:隐患复查
"""
import allure

from common import read_config
from pages.base_page import BasePage


class PendingReviewScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\config\\base_xpath.ini")
    reviewed_tab = readeConfigObj.get_config('review', 'reviewed_tab')  # 已复查标签
    un_review_tab = readeConfigObj.get_config('review', 'un_review_tab')  # 待复查标签
    reviewing_tab = readeConfigObj.get_config('review', 'reviewing_tab')  # 通过·不通过标签
    detail_tab = readeConfigObj.get_config('review', 'detail_tab')  # 详细信息标签
    pass_radio = readeConfigObj.get_config('review', 'pass_radio')  # 通过选择项
    reviewDate = readeConfigObj.get_config('review', 'reviewDate')  # 通过：复查时间
    reviewMan = readeConfigObj.get_config('review', 'reviewMan')  # 通过：复查人
    reviewShift = readeConfigObj.get_config('review', 'reviewShift')  # 通过：复查班次
    rectMeasures = readeConfigObj.get_config('review', 'rectMeasures')  # 通过：复查情况
    rectMeasures_area = readeConfigObj.get_config('review', 'rectMeasures_area')  # 内容输入框
    submit_btn_area = readeConfigObj.get_config('review', 'submit_btn_area')  # 内容输入界面确定按钮
    unPass_radio = readeConfigObj.get_config('review', 'unPass_radio')  # 不通过选择项
    limit_time = readeConfigObj.get_config('review', 'limit_time')  # 不通过：期限日期
    review_time = readeConfigObj.get_config('review', 'review_time')  # 不通过：复查日期
    review_person = readeConfigObj.get_config('review', 'review_person')  # 不通过：复查人
    review_shift = readeConfigObj.get_config('review', 'review_shift')  # 不通过：复查班次
    rect_measures = readeConfigObj.get_config('review', 'rect_measures')  # 不通过：复查情况
    submit_pass_btn = readeConfigObj.get_config('review', 'submit_pass_btn')  # 通过：提交按钮
    submit_unPass_btn = readeConfigObj.get_config('review', 'submit_unPass_btn')  # 不通过：提交按钮

    def review_pass(self, review_date_str, review_man_str, review_shift_str, rect_measures_str):
        """
        复查通过
        :param review_date_str: 复查时间
        :param review_man_str: 复查人
        :param review_shift_str: 复查班次
        :param rect_measures_str: 复查情况内容
        :return:
        """
        with allure.step('选择复查时间:' + review_date_str):
            self.driver.click_element(self.reviewDate)
            self.driver.deal_date_piker(review_date_str)
            self.driver.click_element(self.submit_btn_area)
        with allure.step('选择复查人：' + review_man_str):
            self.driver.choose_attr_value(self.reviewMan, review_man_str)
        with allure.step('选择复查班次：' + review_shift_str):
            self.driver.choose_attr_value(self.reviewShift, review_shift_str)
        with allure.step('录入复查情况内容：' + rect_measures_str):
            self.driver.click_element(self.rectMeasures)
            self.driver.input_text(self.rectMeasures_area, rect_measures_str)
            self.driver.click_element(self.submit_btn_area)
        with allure.step('提交数据'):
            self.driver.click_element(self.submit_pass_btn)

    def review_reject(self, limit_time_str, review_date_str, review_man_str, review_shift_str, rect_measures_str):
        """
        隐患复查不通过
        :param limit_time_str: 期限时间
        :param review_date_str: 复查时间
        :param review_man_str: 复查人
        :param review_shift_str: 复查班次
        :param rect_measures_str: 复查情况
        :return:
        """
        self.driver.click_element(self.unPass_radio)  # 选择不通过标签
        with allure.step('输入期限时间：' + limit_time_str):
            self.driver.click_element(self.limit_time)
            self.driver.deal_date_piker(limit_time_str)
            self.driver.click_element(self.submit_btn_area)
        with allure.step('输入复查时间：' + review_date_str):
            self.driver.click_element(self.review_time)
            self.driver.deal_date_piker(review_date_str)
            self.driver.click_element(self.submit_btn_area)
        with allure.step('选择复查人：' + review_man_str):
            self.driver.choose_attr_value(self.review_person, review_man_str)
        with allure.step('选择复查班次：' + review_shift_str):
            self.driver.choose_attr_value(self.review_shift, review_shift_str)
        with allure.step('录入复查情况内容：' + rect_measures_str):
            self.driver.click_element(self.rect_measures)
            self.driver.input_text(self.rectMeasures_area, rect_measures_str)
            self.driver.click_element(self.submit_btn_area)
        with allure.step('提交数据'):
            self.driver.click_element(self.submit_unPass_btn)
