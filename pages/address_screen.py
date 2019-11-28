# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: address_screen.py
date: 2019/11/28 13:11
Desc: 风险点
"""
import re

from common import read_config
from pages.base_page import BasePage


class AddressScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\data\\base_xpath.ini")
    address_point_name = readeConfigObj.get_config('riskPoint', 'risk_point_name')  # 风险点名称
    hazard_on_address = readeConfigObj.get_config('riskPoint', 'source_on_risk')  # 风险点关联危险源标签
    risk_on_address = readeConfigObj.get_config('riskPoint', 'risk_name')  # 风险点关联风险标签
    depart_on_address = readeConfigObj.get_config('riskPoint', 'unit_on_risk')  # 风险点关联责任部门标签
    tmp_item_source_depart = readeConfigObj.get_config('riskPoint', 'tmp_item_source_depart')  # 危险源列表相关数据
    tmp_item_risk = readeConfigObj.get_config('riskPoint', 'tmp_item_risk')  # 风险列表相关数据

    def get_serial_of_address(self, address_name_str):
        """获取风险点的序号"""
        # 获取所有行的数据 👇
        _tmp_elements = self.driver.get_elements('xpath', "//*[@resource-id='com.universal:id/recyclerView']/android.widget.LinearLayout")
        for _element in _tmp_elements:
            pattern = r'[【|】]'
            _tmp_str = re.split(pattern, _element.find_element_by_id('com.universal:id/text_risk_point_name').text)[1]  # 👈获取危险源名称
            if _tmp_str == address_name_str:
                return _tmp_elements.index(_element)
            continue

    def click_module(self, module_loc, address_name_str):
        """点击指定风险点相对应的标签"""
        _xpath_loc = "xpath>=//*[@resource-id='com.universal:id/recyclerView']/android.widget.LinearLayout[@index='%d']" \
                     % (self.get_serial_of_address(address_name_str))
        _element = self.driver.get_element(_xpath_loc)
        _element.find_element_by_id(module_loc).click()

    def collect_hazard_or_depart_on_address(self):
        """风险点关联的危险源/责任部门"""
        # 查找关联的危险源/ 责任部门 👇
        _source_elements = self.driver.get_elements('xpath', self.tmp_item_source_depart)
        _source_list = []
        # 遍历所有的危险源 / 责任部门，返回找到的危险源 / 责任部门 👇
        for _source in _source_elements:
            _source_list.append(_source.text)
        return _source_list

    def collect_risk_on_address(self):
        """风险点关联的风险"""
        # 查找关联的风险 👇
        _source_elements = self.driver.get_elements('xpath', self.tmp_item_risk)
        _source_list = []
        # 遍历所有的风险，返回找到的风险 👇
        for _source in _source_elements:
            _source_list.extend(self.sub_risk(_source.text))
        return _source_list

    def sub_risk(self, risk_str):
        """截取风险的字段
        返回的字符串类似 '重大风险		应急救援		未检查保险带完好情况'， 截取成类似 ['应急救援', '未检查保险带完好情况'] 的字符串
        """
        _tmp_list = []
        pattern = r'[\t\t]'
        _tmp = re.split(pattern, risk_str)[2::2]
        for item in range(len(_tmp)):
            _tmp_list.append(_tmp[item])
        return _tmp_list
