# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: vio_add_screen.py
date: 2019/11/25 16:37
Desc: 三违录入页面元素配置
"""
import allure

from common import read_config
from pages.base_page import BasePage


class VioAddScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\data\\base_xpath.ini")

    vio_date = readeConfigObj.get_config('vioAdd', 'vio_date')
    vio_address = readeConfigObj.get_config('vioAdd', 'vio_address')
    vio_people = readeConfigObj.get_config('vioAdd', 'vio_people')
    vio_level = readeConfigObj.get_config('vioAdd', 'vio_level')
    find_units = readeConfigObj.get_config('vioAdd', 'find_units')
    vio_desc = readeConfigObj.get_config('vioAdd', 'vio_desc')
    vio_shift = readeConfigObj.get_config('vioAdd', 'vio_shift')
    vio_units = readeConfigObj.get_config('vioAdd', 'vio_units')
    vio_category = readeConfigObj.get_config('vioAdd', 'vio_category')
    vio_qualitative = readeConfigObj.get_config('vioAdd', 'vio_qualitative')
    stop_person = readeConfigObj.get_config('vioAdd', 'stop_person')
    vio_remark = readeConfigObj.get_config('vioAdd', 'vio_remark')
    content_area = readeConfigObj.get_config('vioAdd', 'content_area')
    area_submit_btn = readeConfigObj.get_config('vioAdd', 'area_submit_btn')
    pop_search = readeConfigObj.get_config('vioAdd', 'pop_search')
    vio_submit_btn = readeConfigObj.get_config('vioAdd', 'vio_submit_btn')

    CONTROL_LOC = "class>=android.widget.LinearLayout"

    def choose_vio_date(self, vio_date_str):
        """选择违章时间"""
        with allure.step('选择违章时间：' + vio_date_str):
            self.driver.click_element(self.vio_date)
            self.driver.deal_date_piker(vio_date_str)
            self.driver.click_element(self.area_submit_btn)

    def choose_vio_address(self, vio_address_str):
        """选择违章地点"""
        with allure.step('选择违章地点：' + vio_address_str):
            self.driver.click_element(self.vio_address)
            self.driver.choose_param(vio_address_str, self.CONTROL_LOC)

    def choose_vio_people(self, vio_people_str):
        """选择违章人员"""
        with allure.step('选择违章人员：' + vio_people_str):
            self.driver.click_element(self.vio_people)
            self.driver.choose_param(vio_people_str, self.CONTROL_LOC)

    def choose_vio_level(self, vio_level_str):
        """选择违章级别"""
        with allure.step('选择违章级别：' + vio_level_str):
            self.driver.click_element(self.vio_level)
            self.driver.choose_param(vio_level_str, self.CONTROL_LOC)

    def choose_vio_check_unit(self, vio_check_unit_str):
        """选择三违查处单位"""
        with allure.step('选择三违查处单位：' + vio_check_unit_str):
            self.driver.click_element(self.find_units)
            self.driver.choose_param(vio_check_unit_str, self.CONTROL_LOC)

    def type_vio_desc(self, vio_desc_content):
        with allure.step('输入三违内容'):
            self.driver.click_element(self.vio_desc)
            self.driver.input_text(self.content_area, vio_desc_content)
            self.driver.click_element(self.area_submit_btn)

    def choose_vio_shift(self, vio_shift_str):
        with allure.step('选择班次：' + vio_shift_str):
            self.driver.click_element(self.vio_shift)
            self.driver.choose_param(vio_shift_str, self.CONTROL_LOC)

    def choose_vio_unit(self, vio_unit_str):
        """选择违章单位"""
        with allure.step('选择违章单位：' + vio_unit_str):
            self.driver.click_element(self.vio_units)
            self.driver.choose_param(vio_unit_str, self.CONTROL_LOC)

    def choose_vio_category(self, vio_category_str):
        """选择违章分类"""
        with allure.step('选择违章分类：' + vio_category_str):
            self.driver.click_element(self.vio_category)
            self.driver.choose_param(vio_category_str, self.CONTROL_LOC)

    def choose_vio_qualitative(self, vio_qualitative_str):
        """选择违章定性"""
        with allure.step('选择违章定性：' + vio_qualitative_str):
            self.driver.click_element(self.vio_qualitative)
            self.driver.choose_param(vio_qualitative_str, self.CONTROL_LOC)

    def choose_stop_person(self, stop_person_str):
        """选择制止人"""
        with allure.step('选择制止人：' + stop_person_str):
            self.driver.click_element(self.stop_person)
            self.driver.choose_param(stop_person_str, self.CONTROL_LOC)

    def type_vio_remark(self, vio_remark_content):
        with allure.step('输入三违备注'):
            self.driver.click_element(self.vio_remark)
            self.driver.input_text(self.content_area, vio_remark_content)
            self.driver.click_element(self.area_submit_btn)

    def submit_vio(self):
        with allure.step('提交三违数据'):
            self.driver.click_element(self.vio_submit_btn)
