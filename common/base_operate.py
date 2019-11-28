# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: base_operate.py
date: 2019/11/25 13:49
Desc:封装元素的基本操作
"""
import inspect
import time

import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.log import logger
from common.mysql_operation import ConnMysql

conn = ConnMysql()


def format_screen_shot_time():
    temp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    return temp


class BaseOperate:

    def __init__(self, driver):
        """初始化"""
        self.driver = driver
        self.timeout_time = 15
        self.wait_time = 2

    def get_element(self, type_and_value):
        """定位单个元素"""
        if ">=" not in type_and_value:
            by = "id"
            value = type_and_value
        else:
            attr = type_and_value.split(">=")
            by = attr[0]
            value = attr[1]
        try:
            if by == "id":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_id(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                element = self.driver.find_element_by_id(value)
                return element
            if by == "name":
                find_name = "//*[@text='%s']" % value
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_xpath(find_name).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                element = self.driver.find_element_by_xpath(find_name)
                return element
            if by == "xpath":
                # WebDriverWait(self.driver, self.timeout_time).until(
                #                 #     lambda driver: driver.find_element_by_xpath(value).is_displayed())
                #                 # self.driver.implicitly_wait(self.wait_time)
                element = self.driver.find_element_by_xpath(value)
                return element
            if by == "class":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_class_name(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                element = self.driver.find_element_by_class_name(value)
                return element
            if by == "content":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_accessibility_id(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                element = self.driver.find_element_by_accessibility_id(value)
                return element
            else:
                raise NameError("Please Enter correct element value")
        except NoSuchElementException as msg:
            logger.warning(msg)

    def get_elements(self, by, value):
        """定位一组元素"""
        try:
            if by == "id":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_id(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_elements_by_id(value)
                return elements
            if by == "name":
                find_name = "//*[@text='%s']" % value
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_xpath(find_name).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_elements_by_xpath(find_name)
                return elements
            if by == "xpath":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_xpath(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_elements_by_xpath(value)
                return elements
            if by == "class_name":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_class_name(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_elements_by_class_name(value)
                return elements
            if by == "content":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_accessibility_id(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_elemens_by_accessibility_id(value)
                return elements
            else:
                raise NameError("Please Enter correct elements value")
        except BaseException:
            logger.warning("not find element")

    def click_element(self, value):
        """封装点击操作"""
        element = self.get_element(value)
        element.click()

    def input_text(self, value, text):
        """在文本框输入文本"""
        element = self.get_element(value)
        element.send_keys(text)

    def get_element_text(self, value):
        """获取元素的文本"""
        element = self.get_element(value)
        return element.text

    def get_screen_size(self):
        """获取屏幕分辨率"""
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def get_element_location(self, value):
        """Gets the location of an element relative to the view"""
        location = self.get_element(value).location_in_view
        x = location['x']
        y = location['y']
        return x, y

    def get_element_size(self, value):
        """get the size of the element"""
        size = self.get_element(value).size
        height = size['height']
        width = size['width']
        return height, width

    def get_element_rect(self, value):
        """
        get the size and location of the element
        :param value:
        :return: {'height': 940, 'width': 512, 'x': 208, 'y': 194}
        """
        return self.get_element(value).rect

    def swipe_in_control(self, value, distance, direction='up'):
        """
        控件内滑动.待选择数据较多的情况下可使用
        :param value:
        :param distance:
        :param direction: 滑动方向
        :return:
        """
        start_x, start_y = self.get_element_location(value)
        height_y, width_x = self.get_element_size(value)
        # 向上滑动
        if direction == 'up' or direction == '1':
            point_start_x = start_x + width_x / int(distance)
            point_start_y = start_y + height_y / int(distance)
            self.driver.swipe(
                point_start_x,
                point_start_y,
                point_start_x,
                start_y)
        # 向下滑动
        elif direction == 'down' or direction == '2':
            point_start_x = start_x + width_x / int(distance)
            point_start_y = start_y + height_y / int(distance)
            self.driver.swipe(
                point_start_x,
                start_y,
                point_start_x,
                point_start_y)
        # 往左滑动
        elif direction == 'left' or direction == '3':
            pass
        # 往右滑动
        elif direction == 'right' or direction == '4':
            pass
        else:
            logger.warn('移动方向错误')

    def swipe_up(self, duration=1000):
        """屏幕向上滑动"""
        size = self.get_screen_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.75)
        y2 = int(size[1] * 0.25)
        self.driver.swipe(x1, y1, x1, y2, duration)

    def click_back(self):
        self.driver.press_keycode(4)

    def is_displayed(self, value):
        """判断元素是否在当前页面显示"""
        is_displayed = False
        try:
            is_displayed = self.get_element(value).is_displayed()
        except Exception as e:
            logger.warning(e)
        return is_displayed

    def is_exist_current(self, text):
        """通过获取所有元素来判断当前text是否存在"""
        all_element = self.driver.page_source
        return text in all_element

    def is_toast_exist(self, toast_text):
        """验证toast是否出现"""
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % toast_text)
            WebDriverWait(
                self.driver, 10).until(
                EC.presence_of_element_located(toast_loc))
            return True
        except BaseException:
            return False

    def get_screen_shot(self, case_name):
        """截图"""
        file_name = format_screen_shot_time() + '_' + case_name
        file_path = './screenshots/%s.png' % file_name
        self.driver.get_screenshot_as_file(file_path)
        return file_path

    def quit(self):
        self.driver.quit()

    def assert_in(self, text):
        self.assert_true(self.is_exist_current(text))

    def assert_not_in(self, text):
        self.assert_false(self.is_exist_current(text))

    def assert_true(self, param):
        try:
            assert param is True, "%s is not true" % str(param)
        except Exception as msg:
            file = self.get_screen_shot(str(inspect.stack()[1][3]))
            content = open(file, 'rb').read()
            allure.attach(content, '失败截图', allure.attachment_type.PNG)
            raise AssertionError(msg)

    def assert_false(self, param):
        try:
            assert param is False, "%s is not false" % str(param)
        except Exception as msg:
            file = self.get_screen_shot(str(inspect.stack()[1][3]))
            content = open(file, 'rb').read()
            allure.attach(content, '失败截图', allure.attachment_type.PNG)
            raise AssertionError(msg)

    def assert_equal(self, value1, value2):
        try:
            assert value1 == value2, "%s != %s" % (repr(value1), repr(value2))
        except Exception as msg:
            file = self.get_screen_shot(str(inspect.stack()[1][3]))
            content = open(file, 'rb').read()
            allure.attach(content, '失败截图', allure.attachment_type.PNG)
            raise AssertionError(msg)

    def assert_not_equal(self, value1, value2):
        try:
            assert value1 != value2, "%s != %s" % (repr(value1), repr(value2))
        except Exception as msg:
            file = self.get_screen_shot(str(inspect.stack()[1][3]))
            content = open(file, 'rb').read()
            allure.attach(content, '失败截图', allure.attachment_type.PNG)
            raise AssertionError(msg)

    def assert_dict_equal(self, dict1, dict2):
        """断言：比较两个dict是否相同"""
        try:
            keys1 = dict1.keys()
            keys2 = dict2.keys()
            if len(keys1) == len(keys2) and keys1 == keys2:
                for key in keys1:
                    if dict1[key] == dict2[key]:
                        self.assert_true(dict1[key] == dict2[key])
            else:
                self.assert_false(len(keys1) != len(keys2))
        except Exception as msg:
            raise msg

    def deal_date_piker(self, date_str):
        """处理日期"""
        import re
        pattern = r'[-|/|.]'
        # 使用正则分割时间字符串
        tmp_data = re.split(pattern, date_str)
        _year = tmp_data[0]  # 年
        _month = tmp_data[1]  # 月
        _day = tmp_data[2]  # 日
        _number_pickers = self.get_elements(
            'class_name', 'android.widget.NumberPicker')  # 日期控件
        # year
        current_year_str = _number_pickers[0].find_element_by_id(
            'android:id/numberpicker_input').text
        previous_year_element = _number_pickers[0].find_element_by_xpath(
            "//android.widget.Button[@index='0']")
        while int(_year) != int(current_year_str):
            if int(_year) < int(current_year_str):
                previous_year_element.click()
                tmp_year_str = _number_pickers[0].find_element_by_id(
                    'android:id/numberpicker_input').text
                if int(tmp_year_str) == int(_year):
                    break
                else:
                    previous_year_element.click()

        # month
        current_month_str = _number_pickers[1].find_element_by_id(
            'android:id/numberpicker_input').text
        previous_month_element = _number_pickers[1].find_element_by_xpath(
            "//android.widget.Button[@index='0']")
        next_month_element = _number_pickers[1].find_element_by_xpath(
            "//android.widget.Button[@index='2']")
        while int(current_month_str) != int(_month):
            tmp_month_str = _number_pickers[1].find_element_by_id(
                'android:id/numberpicker_input').text
            if int(tmp_month_str) > int(_month):
                previous_month_element.click()
                tmp_month_str1 = _number_pickers[1].find_element_by_id(
                    'android:id/numberpicker_input').text
                if int(tmp_month_str1) == int(_month):
                    break
                else:
                    previous_month_element.click()
            else:
                tmp_month_str2 = _number_pickers[1].find_element_by_id(
                    'android:id/numberpicker_input').text
                if int(tmp_month_str2) == int(_month):
                    break
                else:
                    next_month_element.click()

        # day
        current_day_str = _number_pickers[2].find_element_by_id(
            'android:id/numberpicker_input').text
        previous_day_element = _number_pickers[2].find_element_by_xpath(
            "//android.widget.Button[@index='0']")
        next_day_element = _number_pickers[2].find_element_by_xpath(
            "//android.widget.Button[@index='2']")
        while int(current_day_str) != int(_day):
            tmp_day_str = _number_pickers[2].find_element_by_id(
                'android:id/numberpicker_input').text
            if int(tmp_day_str) > int(_day):
                previous_day_element.click()
                tmp_day_str1 = _number_pickers[2].find_element_by_id(
                    'android:id/numberpicker_input').text
                if int(tmp_day_str1) == int(_day):
                    break
                else:
                    previous_day_element.click()
            else:
                tmp_day_str2 = _number_pickers[2].find_element_by_id(
                    'android:id/numberpicker_input').text
                if int(tmp_day_str2) == int(_day):
                    break
                else:
                    next_day_element.click()

    def choose_param(self, para_str, control_loc):
        """
        针对较多的待选择的数据时，滑动控件，选择数据
        :param para_str: 带选择的对象的text
        :param control_loc: 控件loc， 使用class>=android.widget.LinearLayout的形式表示
        :return:
        """
        _tmp = "xpath>=//*[@resource-id='com.universal:id/text' and @text = '%s']" % para_str
        while True:
            if self.is_displayed(_tmp):
                self.click_element(_tmp)
                break
            else:
                self.swipe_in_control(control_loc, 2, 'up')
                if self.is_displayed(_tmp):
                    self.click_element(_tmp)
                    break

    # @staticmethod
    def collect_detail_of_risk(self, hazard_name):
        """处理风险详情"""
        details = {}  # 用于存放风险详情内容
        tmp_detail_list = []
        tmp_key_list = (
            '辨识时间',
            '隐患描述',
            '专业',
            '危险源名称',
            '作业活动',
            '风险描述',
            '风险等级',
            '风险类型',
            '管控标准来源',
            '章节条款',
            '标准内容',
            '管控措施',
            '责任岗位',
            '罚款金额')
        from data import sql_constants
        tmp_detail = conn.get_infos(
            sql_constants.detail_of_risk_sql(hazard_name))[0]  # 查询得到部分内容

        for index in tmp_detail:
            tmp_detail_list.append(index)

        tmp_detail_list[0] = tmp_detail_list[0][:10]  # 处理辨识时间

        for index in tmp_key_list:
            details[index] = tmp_detail_list[tmp_key_list.index(index)]

        # 处理伤害类别 👇，伤害类别可以是多个
        _damage_type_code = tuple(
            conn.get_info(
                sql_constants.damage_type_code_sql(hazard_name)).split(','))  # 伤害类别代码
        _tmp_damage_type = conn.get_infos(
            sql_constants.damage_type_value_sql(_damage_type_code))
        _damage_type = []  # 伤害类别
        for i in _tmp_damage_type:
            for _type_d in i:
                _damage_type.append(_type_d)
        details['伤害类别'] = self.sub_on_damage_or_accident(_damage_type)  # 将伤害类别添加到详情中  👆
        # 处理事故类型 👇， 事故类型可能是多个
        _accident_type_code = tuple(conn.get_info(
            sql_constants.ye_accident_code_sql(hazard_name)).split(','))  # 事故类型代码
        _tmp_accident_type = conn.get_infos(
            sql_constants.ye_accident_value_sql(_accident_type_code))
        _accident_type = []
        for i in _tmp_accident_type:
            for _type_a in i:
                _accident_type.append(_type_a)
        details['事故类型'] = self.sub_on_damage_or_accident(_accident_type)  # 将事故类型添加到详情中 👆
        details['隐患等级'] = conn.get_info(sql_constants.risk_level_value_sql(hazard_name))  # 添加隐患等级
        return details

    def sub_on_damage_or_accident(self, para):
        """dict to str"""
        _str = ''
        for i in range(len(para)):
            _str = _str + ''.join(para[i]) + ','
        return _str[:-1]
