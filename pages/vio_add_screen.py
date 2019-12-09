# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: vio_add_screen.py
date: 2019/11/25 16:37
Desc: 三违录入页面元素配置
"""
import random

import allure

from common import read_config
from common.log import logger
from pages.base_page import BasePage
from common.mysql_operation import ConnMysql

conn = ConnMysql()


class VioAddScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\config\\base_xpath.ini")

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
    vio_date_item = readeConfigObj.get_config('vioAdd', 'vio_date_item')
    vio_address_item = readeConfigObj.get_config('vioAdd', 'vio_address_item')
    vio_unit_item = readeConfigObj.get_config('vioAdd', 'vio_unit_item')
    vio_desc_item = readeConfigObj.get_config('vioAdd', 'vio_desc_item')
    uploaded_tab = readeConfigObj.get_config('vioAdd', 'uploaded_tab')  # 已上报标签
    image_select = readeConfigObj.get_config('image', 'image_select')   # 上传图片按钮
    select_photo = readeConfigObj.get_config('image', 'select_photo')  # 选择图片标签
    photo_select_checkbox = readeConfigObj.get_config('image', 'photo_select')  # 图片选择checkbox
    submit_photo = readeConfigObj.get_config('image', 'submit_photo')  # 提交已选择的图片

    CONTROL_LOC = "class>=android.widget.LinearLayout"  # 弹窗

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

    def upload_images(self, max_nums):
        """
        选择图片
        :param max_nums: 上传图片数量
        :return:
        """
        with allure.step('选择相关图片信息：'):
            self.driver.click_element(self.image_select)
            self.driver.click_element(self.select_photo)
            photo_elements = self.driver.get_elements('id', self.photo_select_checkbox)
            for photo in photo_elements:  # 从第一张图片开始从左到右从上到下选择图片
                photo.click()
                if photo_elements.index(photo) == int(max_nums):
                    break
            self.driver.click_element(self.submit_photo)
            if max_nums >= 3:  # 当图片数量大于3张时需要向上滑动界面，显示‘保存’按钮
                self.driver.swipe_up()

    def submit_vio(self):
        with allure.step('提交三违数据'):
            self.driver.click_element(self.vio_submit_btn)

    def collect_detail_of_vio(self):
        """获取app中三违详情内容"""
        detail_dic = {}  # 用于存放详情内容
        _xpath_loc = "//*[@class = 'android.widget.ScrollView']/android.widget.LinearLayout/android.widget.LinearLayout"  # key-value loc
        _key_loc = "//android.widget.TextView[@index='0']"  # 属性字段loc
        _value_loc = "//android.widget.TextView[@index='1']"  # 属性值loc
        _elements = self.driver.get_elements('xpath', _xpath_loc)  # 查找三违详情相关的key和value
        for _element in _elements:
            _key_content = _element.find_element_by_xpath(_key_loc).text[:-1]
            _value_content = _element.find_element_by_xpath(_value_loc).text
            detail_dic[_key_content] = _value_content
        return detail_dic

    def collect_detail_of_vio_from_db(self, vio_date, vio_address, vio_unit, vio_desc):
        """获取数据库中三违详情内容"""
        details = {}  # 用于存放风险详情内容
        tmp_detail_list = []  # 存放临时变量
        tmp_key_list = ('违章时间', '违章地点', '违章人员', '违章定性', '制止人', '违章单位', '违章分类', '三违级别', '查处单位', '三违事实描述', '备注')

        from config import sql_constants
        tmp_detail = conn.get_infos(sql_constants.detail_of_vio_sql(vio_date, vio_address, vio_unit, vio_desc))[0]  # 通过查询得到详情内容
        for _index in tmp_detail:
            tmp_detail_list.append(_index)

        tmp_detail_list[0] = tmp_detail_list[0][:10]  # 处理辨识时间, 截取年月日

        for _index in tmp_key_list:  # 将数据保存到details中
            details[_index] = tmp_detail_list[tmp_key_list.index(_index)]
        return details

    def choose_and_click_vio(self, vio_date, vio_address, vio_unit, vio_desc):
        """点击指定的三违数据"""
        _vio_xpath_loc = "//*[@resource-id='com.universal:id/recyclerView']/android.widget.RelativeLayout"
        _vio_elements = self.driver.get_elements('xpath', _vio_xpath_loc)  # 获取当前界面上三违
        for _element in _vio_elements:
            _date_text = ''.join(_element.find_element_by_id(self.vio_date_item).text.split())[5:]  # 违章时间
            _address_text = ''.join(_element.find_element_by_id(self.vio_address_item).text.split())[5:]  # 违章地点
            _unit_text = ''.join(_element.find_element_by_id(self.vio_unit_item).text.split())[5:]  # 违章单位
            _desc_text = _element.find_element_by_id(self.vio_desc_item).text  # 三违内容描述
            if _date_text == vio_date and _address_text == vio_address and _unit_text == vio_unit and _desc_text == vio_desc:
                _element.click()
                break

    def get_vio_params(self):
        """获取三违参数，依次返回三违时间/地点/单位/三违内容"""
        _vio_xpath_loc = "//*[@resource-id='com.universal:id/recyclerView']/android.widget.RelativeLayout"
        _vio_elements = self.driver.get_elements('xpath', _vio_xpath_loc)  # 获取当前界面上三违
        if len(_vio_elements) > 0:
            _index = random.randint(0, len(_vio_elements) - 1)
            _date_text = ''.join(_vio_elements[_index].find_element_by_id(self.vio_date_item).text.split())[5:]  # 违章时间
            _address_text = ''.join(_vio_elements[_index].find_element_by_id(self.vio_address_item).text.split())[5:]  # 违章地点
            _unit_text = ''.join(_vio_elements[_index].find_element_by_id(self.vio_unit_item).text.split())[5:]  # 违章单位
            _desc_text = _vio_elements[_index].find_element_by_id(self.vio_desc_item).text  # 三违内容描述
            return _date_text, _address_text, _unit_text, _desc_text
        else:
            logger.warning('no vio config')
