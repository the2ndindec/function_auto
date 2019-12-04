# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: hidden_danger_screen.py
date: 2019/11/29 10:40
Desc: 隐患录入
"""
import allure

from common import read_config
from common.mysql_operation import ConnMysql
from pages.base_page import BasePage

conn = ConnMysql()


class HiddenDangerScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\data\\base_xpath.ini")
    uploaded_tab = readeConfigObj.get_config('hiddenDanger', 'uploaded_tab')
    exam_type = readeConfigObj.get_config('hiddenDanger', 'exam_type')
    exam_date = readeConfigObj.get_config('hiddenDanger', 'exam_date')
    exam_shift = readeConfigObj.get_config('hiddenDanger', 'exam_shift')
    exam_address = readeConfigObj.get_config('hiddenDanger', 'exam_address')
    exam_check_man = readeConfigObj.get_config('hiddenDanger', 'exam_check_man')
    exam_duty_unit = readeConfigObj.get_config('hiddenDanger', 'exam_duty_unit')
    exam_duty_man = readeConfigObj.get_config('hiddenDanger', 'exam_duty_man')
    exam_hidden_category = readeConfigObj.get_config('hiddenDanger', 'exam_hidden_category')
    exam_hidden_level = readeConfigObj.get_config('hiddenDanger', 'exam_hidden_level')
    exam_hidden_type = readeConfigObj.get_config('hiddenDanger', 'exam_hidden_type')
    exam_problem_desc = readeConfigObj.get_config('hiddenDanger', 'exam_problem_desc')
    problem_desc_area = readeConfigObj.get_config('hiddenDanger', 'problem_desc_area')
    submit_btn_area = readeConfigObj.get_config('hiddenDanger', 'submit_btn_area')
    deal_type_limit = readeConfigObj.get_config('hiddenDanger', 'deal_type_limit')
    limit_date = readeConfigObj.get_config('hiddenDanger', 'limit_date')
    deal_type_current = readeConfigObj.get_config('hiddenDanger', 'deal_type_current')
    review_man = readeConfigObj.get_config('hiddenDanger', 'review_man')
    exam_save_btn = readeConfigObj.get_config('hiddenDanger', 'exam_save_btn')
    item_list = readeConfigObj.get_config('hiddenDanger', 'item_list')
    item_value = readeConfigObj.get_config('hiddenDanger', 'item_value')

    CONTROL_LOC = "class>=android.widget.LinearLayout"  # 弹窗

    """！！！检查类型为上级检查时，检查人需要手动输入"""

    # def choose_attr_value(self, attr, attr_value):
    #     """选择属性参数"""
    #     self.driver.click_element(attr)
    #     self.driver.choose_param(attr_value, self.CONTROL_LOC)

    def choose_vio_date(self, exam_date_str):
        """选择检查时间"""
        with allure.step('选择检查时间：' + exam_date_str):
            self.driver.click_element(self.exam_date)
            self.driver.deal_date_piker(exam_date_str)
            self.driver.click_element(self.submit_btn_area)

    def type_hidden_desc(self, hidden_desc_str):
        """输入隐患内容"""
        self.driver.click_element(self.exam_problem_desc)
        self.driver.input_text(self.problem_desc_area, hidden_desc_str)
        self.driver.click_element(self.submit_btn_area)

    def choose_deal_type(self, type_str, **kwargs):
        """隐患处理方式"""
        self.driver.swipe_up()  # 滑动界面
        if type_str == 'limit' or type_str == 'xq':
            # if 'limit_date_str' in kwargs:
            if kwargs:  # 判断是否包含其他参数
                self.driver.click_element(self.limit_date)
                self.driver.deal_date_piker(kwargs[list(kwargs)[0]])
                self.driver.click_element(self.submit_btn_area)
            else:
                raise ValueError('未指定期限时间')
        elif type_str == 'current' or type_str == 'xc':
            self.driver.click_element(self.deal_type_current)
            # if 'review_man_str' in kwargs:
            if kwargs:  # 判断是否包含其他参数
                self.driver.choose_attr_value(self.review_man, kwargs[list(kwargs)[0]])
            else:
                raise ValueError('未指定负责人')
        else:
            raise ValueError("参数‘type_str’错误：", type_str)

    # def collect_detail_of_hidden(self):
    #     """获取隐患详情内容"""
    #     global _key_content
    #     detail_dic = {}  # 用于存放详情内容
    #     _xpath_loc = "//*[@class = 'android.widget.ScrollView']/android.widget.LinearLayout/android.widget.LinearLayout"  # key-value loc
    #     _key_loc = "//android.widget.TextView[@index='0']"  # 属性字段loc
    #     _value_loc = "//android.widget.TextView[@index='1']"  # 属性值loc
    #
    #     _elements = self.driver.get_elements('xpath', _xpath_loc)  # 查找三违详情相关的key和value
    #
    #     # pattern = r'[\t\t]'
    #     # import re
    #     for _element in _elements:
    #         if _element.find_element_by_xpath(_key_loc).text != '复查人':  # 隐患类型为现场处理时，不需要截取字符串
    #             _key_content = _element.find_element_by_xpath(_key_loc).text[:-1].replace('\t', '')
    #         else:
    #             _key_content = _element.find_element_by_xpath(_key_loc).text
    #         if '隐患处理' == _key_content:  # 去掉 ‘隐患处理’
    #             continue
    #
    #         _value_content = _element.find_element_by_xpath(_value_loc).text
    #         detail_dic[_key_content] = _value_content
    #
    #     self.driver.swipe_up()  # 滑动屏幕获取剩下的参数 👇
    #     _elements = self.driver.get_elements('xpath', _xpath_loc)  # 查找三违详情相关的key和value
    #     for _element in _elements:
    #         if _element.find_element_by_xpath(_key_loc).text != '复查人':
    #             _key_content = _element.find_element_by_xpath(_key_loc).text[:-1].replace('\t', '')
    #         else:
    #             _key_content = _element.find_element_by_xpath(_key_loc).text
    #         if '隐患处理' == _key_content:
    #             continue
    #         _value_content = _element.find_element_by_xpath(_value_loc).text
    #         detail_dic[_key_content] = _value_content
    #
    #     return detail_dic

    # def collect_detail_of_hidden_from_db(self, exam_date, exam_type, exam_desc, **kwargs):
    #     """数据库中隐患详情"""
    #     details = {}  # 用于存放风险详情内容
    #     tmp_detail_list = []  # 存放临时变量
    #     tmp_limit_key_list = ('检查类型', '检查时间', '班次', '地点', '检查人', '责任单位', '责任人', '隐患类别', '隐患等级', '隐患类型', '限期日期', '问题描述')
    #     tmp_current_key_list = ('检查类型', '检查时间', '班次', '地点', '检查人', '责任单位', '责任人', '隐患类别', '隐患等级', '隐患类型', '复查人', '问题描述')
    #
    #     from data import sql_constants
    #     _tmp_deal_type = conn.get_info(sql_constants.get_deal_type(exam_desc, exam_type, exam_date))
    #     tmp_detail = conn.get_infos(sql_constants.detail_of_hidden(exam_desc, exam_type, exam_date))[0]  # 通过查询得到详情内容
    #
    #     for _detail in tmp_detail:
    #         tmp_detail_list.append(_detail)
    #
    #     if _tmp_deal_type == '1':
    #         """处理限期整改的隐患"""
    #         tmp_detail_list[1] = tmp_detail_list[1][:10]  # 处理检查时间, 截取年月日
    #         tmp_detail_list[-2] = tmp_detail_list[-2][:10]  # 处理限期日期, 截取年月日
    #         for _key in tmp_limit_key_list:
    #             details[_key] = tmp_detail_list[tmp_limit_key_list.index(_key)]
    #
    #     if _tmp_deal_type == '2':
    #         """处理现场整改的隐患"""
    #         tmp_detail_list[1] = tmp_detail_list[1][:10]  # 处理检查时间, 截取年月日
    #         for _index in tmp_current_key_list:  # 将数据保存到details中
    #             details[_index] = tmp_detail_list[tmp_current_key_list.index(_index)]
    #
    #     return details


if __name__ == '__main__':
    h = HiddenDangerScreen(BasePage)
    print(h.collect_detail_of_hidden_from_db(exam_desc='现场', exam_type='矿领导带班', exam_date='2019-11-29'))

