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
    readeConfigObj = read_config.ReadConfig(r"\config\base_xpath.ini")
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

    def type_exam_check_man(self, check_man_str):
        """录入检查人"""
        self.driver.click_element(self.exam_check_man)
        self.driver.input_text(self.problem_desc_area, check_man_str)
        self.driver.click_element(self.submit_btn_area)

    def choose_deal_type(self, type_str, **kwargs):
        """隐患处理方式"""
        self.driver.swipe_up()  # 滑动界面
        if type_str == 'limit' or type_str == 'xq':  # 限期整改
            if kwargs:  # 选择限定时间
                self.driver.click_element(self.limit_date)
                self.driver.deal_date_piker(kwargs[list(kwargs)[0]])
                self.driver.click_element(self.submit_btn_area)
            else:
                raise ValueError('未指定期限时间')
        elif type_str == 'current' or type_str == 'xc':  # 现场整改
            self.driver.click_element(self.deal_type_current)
            if kwargs:  # 选择复查人
                self.driver.choose_attr_value(self.review_man, kwargs[list(kwargs)[0]])
            else:
                raise ValueError('未指定复查人')
        else:
            raise ValueError("参数‘type_str’错误：", type_str)


if __name__ == '__main__':
    h = HiddenDangerScreen(BasePage)
    print(h.collect_detail_of_hidden_from_db(exam_desc='现场', exam_type='矿领导带班', exam_date='2019-11-29'))

