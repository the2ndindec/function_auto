# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: major_risk_screen.py
date: 2019/11/27 10:07
Desc: 重大风险清单
"""
import time

from common import read_config
from pages.base_page import BasePage


class MajorRiskScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\config\\base_xpath.ini")
    riskPoint = readeConfigObj.get_config('major', 'riskPoint')  # 关联风险点标签
    risk_point_text = readeConfigObj.get_config('major', 'risk_point_text')  # 弹窗中风险点名称字段
    riskManage = readeConfigObj.get_config('major', 'riskManage')  # 管控措施标签
    risk_source_name = readeConfigObj.get_config('major', 'risk_source_name')  # 危险源名称
    risk_manage_group = readeConfigObj.get_config('major', 'risk_manage_group')

    def click_module(self, module_loc, hazard_name_str):
        """点击指定危险源相对应的标签"""
        time.sleep(1)
        try:
            _index = self.get_serial_of_danger(hazard_name_str)
            _xpath_loc = "xpath>=//android.widget.LinearLayout[@index='%d']" % (int(_index))
            element = self.driver.get_element(_xpath_loc)
            element.find_element_by_id(module_loc).click()
        except TypeError as msg:
            raise msg

    def collect_risk_point_on_hazard(self):
        """获取危险源关联的风险点"""
        # fixme 关联数据为空
        _risk_points = self.driver.get_elements('id', self.risk_point_text)
        risk_point_list = []
        if _risk_points:
            for element in _risk_points:
                risk_point_list.append(element.text)
            return risk_point_list
        else:
            return risk_point_list

    def get_serial_of_danger(self, hazard_name_str):
        """获取指定危险源所在行的序列号"""
        # 获取所有行的数据↓
        _tmp_elements = self.driver.get_elements('xpath', "//*[@resource-id='com.universal:id/recyclerView']/android.widget.LinearLayout")
        # 判断每行中危险源的字段值是否和指定的危险源名称一致
        for element in _tmp_elements:
            _tmp_str = element.find_element_by_id('com.universal:id/text_risk_source_name').text
            # 若名称一致，返回该危险源所在行的序列号
            if _tmp_str[1:-1] == hazard_name_str:
                return _tmp_elements.index(element)
            continue

    def collect_manage_on_hazard(self):
        """获取指定危险源关联的管控措施"""
        manage_list = []  # 用于存放所有关联的管控措施的相关内容
        _manages = self.driver.get_elements('xpath', self.risk_manage_group)
        for manage in _manages:
            _controller = manage.find_element_by_id('com.universal:id/text_controller').text
            _achieveEffect = manage.find_element_by_id('com.universal:id/text_achieveEffect').text
            _workContent = manage.find_element_by_id('com.universal:id/text_workContent').text
            manage_tuple = (_controller, _achieveEffect, _workContent)
            manage_list.append(manage_tuple)
            continue
        return manage_list

    def collect_detail_of_risk(self):
        """获取风险详情内容"""
        detail_dic = {}  # 用于存放详情内容
        _xpath_loc = "//*[@class = 'android.widget.ScrollView']/android.widget.LinearLayout/android.widget.LinearLayout"  # key-value loc
        _key_loc = "//android.widget.TextView[@index='0']"
        _value_loc = "//android.widget.TextView[@index='1']"
        _elements = self.driver.get_elements('xpath', _xpath_loc)  # 查找风险相关的key和value
        for _element in _elements:
            _key_content = _element.find_element_by_xpath(_key_loc).text[:-1]
            _value_content = _element.find_element_by_xpath(_value_loc).text
            if _key_content in ('风险状态', '关联风险点数量', '风险点数组', '重大风险管控记录条数', '重大风险管控记录'):  # 👈 这几个字段值不需要
                continue
            detail_dic[_key_content] = _value_content
        # 滑动屏幕获取余下的详情内容
        self.driver.swipe_up()
        _elements = self.driver.get_elements('xpath', _xpath_loc)  # 查找风险相关的key和value
        for _element in _elements:
            _key_content = _element.find_element_by_xpath(_key_loc).text[:-1]
            _value_content = _element.find_element_by_xpath(_value_loc).text
            if _key_content in ('风险状态', '关联风险点数量', '风险点数组', '重大风险管控记录条数', '重大风险管控记录'):  # 👈 这几个字段值不需要
                continue
            detail_dic[_key_content] = _value_content
        return detail_dic

