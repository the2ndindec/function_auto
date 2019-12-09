# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: base_operate.py
date: 2019/11/25 13:49
Desc:封装元素的基本操作
"""
import inspect
import re
import time
import random

import allure
from faker import Faker
from selenium.common.exceptions import NoSuchElementException, InvalidElementStateException, StaleElementReferenceException
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
            logger.warning('[no element on the screen]', msg)

    def get_elements(self, by, value):
        """定位一组元素"""
        try:
            if by == "id":
                WebDriverWait(self.driver, self.timeout_time).until(lambda driver: driver.find_element_by_id(value).is_displayed())
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
        except Exception as msg:
            logger.warning("not find element！", msg)
            return None

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
        try:
            location = self.get_element(value).location_in_view
            x = location['x']
            y = location['y']
            return x, y
        except AttributeError as msg:
            raise msg

    def get_element_size(self, value):
        """get the size of the element"""
        try:
            size = self.get_element(value).size
            height = size['height']
            width = size['width']
            return height, width
        except AttributeError as msg:
            raise msg

    def get_element_rect(self, value):
        """
        get the size and location of the element
        :param value:
        :return: {'height': 940, 'width': 512, 'x': 208, 'y': 194}
        """
        return self.get_element(value).rect

    """Swipe from one point to another point, for an optional duration.

            Args:
                start_x (int): x-coordinate at which to start
                start_y (int): y-coordinate at which to start
                end_x (int): x-coordinate at which to stop
                end_y (int): y-coordinate at which to stop
                duration (:obj:`int`, optional): time to take the swipe, in ms.

            Usage:
                driver.swipe(100, 100, 100, 400)

            Returns:
                `appium.webdriver.webelement.WebElement`
     """

    def swipe_in_control(self, value, distance, direction='up'):
        """
        控件内滑动.待选择数据较多的情况下可使用
        :param value: 元素loc
        :param distance: 滑动距离 ， 1表示滑动全屏， 2表示滑动一半， 3表示滑动1/3，以此类推
        :param direction: 滑动方向
        :return:
        """
        start_x, start_y = self.get_element_location(value)
        height_y, width_x = self.get_element_size(value)
        # 屏幕向上滑动
        if direction == 'up' or direction == '1':
            point_start_x = start_x + width_x / int(distance)
            point_start_y = start_y + height_y / int(distance)
            self.driver.swipe(
                point_start_x,
                point_start_y,
                point_start_x,
                start_y)
        # 屏幕向下滑动 ，可用于刷新页面/数据
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
        try:
            size = self.get_screen_size()
            x1 = int(size[0] * 0.5)
            y1 = int(size[1] * 0.75)
            y2 = int(size[1] * 0.25)
            self.driver.swipe(x1, y1, x1, y2, duration)
        except InvalidElementStateException as msg:
            raise msg

    def click_back(self):
        self.driver.press_keycode(4)
        time.sleep(1)

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
        except Exception as msg:
            logger.warning(msg)
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
        """断言：判断文本字符串是否存在"""
        self.assert_true(self.is_exist_current(text))

    def assert_not_in(self, text):
        """断言：判断文本字符串是否不存在"""
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
            # else:
            #     self.assert_false(len(keys1) != len(keys2))
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
        _number_pickers = self.get_elements('class_name', 'android.widget.NumberPicker')  # 日期控件
        # year
        try:
            current_year_str = _number_pickers[0].find_element_by_id('android:id/numberpicker_input').text
            previous_year_element = _number_pickers[0].find_element_by_xpath("//android.widget.Button[@index='0']")
            while int(_year) != int(current_year_str):
                if int(_year) < int(current_year_str):
                    previous_year_element.click()
                    tmp_year_str = _number_pickers[0].find_element_by_id('android:id/numberpicker_input').text
                    if int(tmp_year_str) == int(_year):
                        break
                    else:
                        previous_year_element.click()
        except Exception as msg:
            logger.warning(msg)

        # month
        try:
            current_month_str = _number_pickers[1].find_element_by_id('android:id/numberpicker_input').text
            previous_month_element = _number_pickers[1].find_element_by_xpath("//android.widget.Button[@index='0']")
            next_month_element = _number_pickers[1].find_element_by_xpath("//android.widget.Button[@index='2']")
            while int(current_month_str) != int(_month):
                tmp_month_str = _number_pickers[1].find_element_by_id('android:id/numberpicker_input').text
                if int(tmp_month_str) > int(_month):
                    previous_month_element.click()
                    tmp_month_str1 = _number_pickers[1].find_element_by_id('android:id/numberpicker_input').text
                    if int(tmp_month_str1) == int(_month):
                        break
                    else:
                        previous_month_element.click()
                else:
                    tmp_month_str2 = _number_pickers[1].find_element_by_id('android:id/numberpicker_input').text
                    if int(tmp_month_str2) == int(_month):
                        break
                    else:
                        next_month_element.click()
        except Exception as msg:
            logger.warning(msg)

        # day
        try:
            current_day_str = _number_pickers[2].find_element_by_id('android:id/numberpicker_input').text
            previous_day_element = _number_pickers[2].find_element_by_xpath("//android.widget.Button[@index='0']")
            next_day_element = _number_pickers[2].find_element_by_xpath("//android.widget.Button[@index='2']")
            while int(current_day_str) != int(_day):
                tmp_day_str = _number_pickers[2].find_element_by_id('android:id/numberpicker_input').text
                if int(tmp_day_str) > int(_day):
                    previous_day_element.click()
                    tmp_day_str1 = _number_pickers[2].find_element_by_id('android:id/numberpicker_input').text
                    if int(tmp_day_str1) == int(_day):
                        break
                    else:
                        previous_day_element.click()
                else:
                    tmp_day_str2 = _number_pickers[2].find_element_by_id('android:id/numberpicker_input').text
                    if int(tmp_day_str2) == int(_day):
                        break
                    else:
                        next_day_element.click()
        except Exception as msg:
            logger.warning(msg)

    def choose_param(self, para_str, control_loc):
        """
        针对较多的待选择的数据时，滑动控件，选择数据
        :param para_str: 带选择的对象的text
        :param control_loc: 控件loc， 使用class>=android.widget.LinearLayout的形式表示
        :return:
        """
        _tmp = "xpath>=//*[@resource-id='com.universal:id/text' and @text = '%s']" % para_str
        while True:
            if self.is_displayed(_tmp):  # fixme 当选择的数据未显示在当前界面上时，会出现Exception
                self.click_element(_tmp)
                break
            else:
                self.swipe_in_control(control_loc, 2, 'up')
                if self.is_displayed(_tmp):
                    self.click_element(_tmp)
                    break

    def collect_detail_of_risk(self, hazard_name):
        """数据库中风险详情"""
        details = {}  # 用于存放风险详情内容
        tmp_detail_list = []  # 存放临时变量
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
        from config import sql_constants
        tmp_detail = conn.get_infos(sql_constants.detail_of_risk_sql(hazard_name))[0]  # 查询得到部分内容

        for _index in tmp_detail:
            tmp_detail_list.append(_index)

        tmp_detail_list[0] = tmp_detail_list[0][:10]  # 处理辨识时间

        for _index in tmp_key_list:
            details[_index] = tmp_detail_list[tmp_key_list.index(_index)]

        # 处理伤害类别 👇，伤害类别可以是多个
        _damage_type_code = tuple(conn.get_info(sql_constants.damage_type_code_sql(hazard_name)).split(','))  # 伤害类别代码
        _tmp_damage_type = conn.get_infos(sql_constants.damage_type_value_sql(_damage_type_code))
        _damage_type = []  # 伤害类别
        for i in _tmp_damage_type:
            for _type_d in i:
                _damage_type.append(_type_d)
        details['伤害类别'] = self.sub_on_damage_or_accident(_damage_type)  # 将伤害类别添加到详情中  👆
        # 处理事故类型 👇， 事故类型可能是多个，也可能为空
        global _accident_type  # update on 12/06
        tmp_accident_type = conn.get_info(sql_constants.ye_accident_code_sql(hazard_name))
        if tmp_accident_type:
            _accident_type_code = tuple(tmp_accident_type.split(','))  # 事故类型代码
            _tmp_accident_type = conn.get_infos(sql_constants.ye_accident_value_sql(_accident_type_code))
            _accident_type = []
            for i in _tmp_accident_type:
                for _type_a in i:
                    _accident_type.append(_type_a)
        else:
            _accident_type = ''
        details['事故类型'] = self.sub_on_damage_or_accident(_accident_type)  # 将事故类型添加到详情中 👆
        # 添加隐患等级
        tmp_level = conn.query(sql_constants.risk_level_value_sql(hazard_name), fetchone=True)
        if tmp_level:
            details['隐患等级'] = tmp_level
        else:
            details['隐患等级'] = ''
        return details

    def sub_on_damage_or_accident(self, para):
        """dict to str"""
        _str = ''
        for i in range(len(para)):
            _str = _str + ''.join(para[i]) + ','
        return _str[:-1]

    def scroll_and_click_element(self, exam_date, exam_type, exam_desc, **kwargs):
        """
        根据指定的参数获取隐患数据. 以下参数通过get_paras_of_hidden方法获取，避免脚本出现问题。
        :param exam_date: 日期
        :param exam_type: 检查类型
        :param exam_desc: 隐患描述
        :param kwargs: 其他，比如责任单位
        :return:
        """
        global _tmp_elements
        # 先获取当前界面上所有的数据
        if not kwargs:  # 适用于隐患录入时查看详情
            _tmp_elements = self.get_elements('xpath', "//*[@resource-id='com.universal:id/recyclerView']/android.widget.RelativeLayout")
        else:
            _tmp_elements = self.get_elements('xpath', "//*[@resource-id='com.universal:id/list_view']/android.widget.RelativeLayout")

        try:
            # 循环当前界面上的数据，匹配到指定参数的数据
            for _element in _tmp_elements:  # fixme 滑动屏幕会导致StaleElementReferenceException

                # if not kwargs:  # 适用于隐患录入时查看详情
                #     _tmp_elements = self.get_elements('xpath', "//*[@resource-id='com.universal:id/recyclerView']/android.widget.RelativeLayout")
                # else:
                #     _tmp_elements = self.get_elements('xpath', "//*[@resource-id='com.universal:id/list_view']/android.widget.RelativeLayout")

                _date = _element.find_element_by_id('com.universal:id/text_date').text
                _type = _element.find_element_by_id('com.universal:id/text_check').text
                _desc = _element.find_element_by_id('com.universal:id/text_describe').text
                # 判断是否包含其他参数
                if kwargs:
                    _unit = _element.find_element_by_id('com.universal:id/text_unit').text
                    if _date == exam_date and _type == exam_type and _desc == exam_desc and _unit == kwargs[list(kwargs)[0]]:
                        _element.click()
                        return
                    # else:
                    #     while self.is_exist_current(exam_date) and self.is_exist_current(
                    #             exam_type) and self.is_exist_current(exam_desc) and self.is_exist_current(kwargs[list(kwargs)[0]]):
                    #         # self.swipe_in_control("com.universal:id/view_pager", 3)
                    #         self.swipe_up()
                    #         _tmp_elements_after = self.get_elements(
                    #             'xpath',
                    #             "//*[@resource-id='com.universal:id/list_view']/android.widget.RelativeLayout")
                    #         for _element_after in _tmp_elements_after:
                    #             _date = _element_after.find_element_by_id('com.universal:id/text_date').text
                    #             _type = _element_after.find_element_by_id('com.universal:id/text_check').text
                    #             _desc = _element_after.find_element_by_id('com.universal:id/text_describe').text
                    #             _unit = _element_after.find_element_by_id('com.universal:id/text_unit').text
                    #             if _date == exam_date and _type == exam_type and _desc == exam_desc and _unit == kwargs[list(kwargs)[0]]:
                    #                 _element_after.click()
                    #                 return

                if _date == exam_date and _type == exam_type and _desc == exam_desc:
                    _element.click()
                    break
                # else:
                #     while self.is_exist_current(exam_date) and self.is_exist_current(exam_type) and self.is_exist_current(exam_desc):
                #         # self.swipe_in_control("com.universal:id/list_view", 2)
                #         self.swipe_up()
                #         _tmp_elements_after = self.get_elements(
                #             'xpath',
                #             "//*[@resource-id='com.universal:id/recyclerView']/android.widget.RelativeLayout")
                #         for _element_after in _tmp_elements_after:
                #             _date = _element_after.find_element_by_id('com.universal:id/text_date').text
                #             _type = _element_after.find_element_by_id('com.universal:id/text_check').text
                #             _desc = _element_after.find_element_by_id('com.universal:id/text_describe').text
                #             if _date == exam_date and _type == exam_type and _desc == exam_desc:
                #                 _element_after.click()
                #                 break
        except StaleElementReferenceException as msg:
            logger.warning(msg)

    CONTROL_LOC = "class>=android.widget.LinearLayout"  # 弹窗

    def choose_attr_value(self, attr, attr_value):
        """选择属性参数"""
        self.click_element(attr)
        self.choose_param(attr_value, self.CONTROL_LOC)

    def collect_detail_of_hidden(self):
        """获取隐患详情内容"""
        global _key_content
        detail_dic = {}  # 用于存放详情内容
        # key-value loc
        _xpath_loc = "//*[@class = 'android.widget.ScrollView']/android.widget.LinearLayout/android.widget.LinearLayout"
        _key_loc = "//android.widget.TextView[@index='0']"  # 属性字段loc
        _value_loc = "//android.widget.TextView[@index='1']"  # 属性值loc

        _elements = self.get_elements('xpath', _xpath_loc)  # 查找三违详情相关的key和value

        # pattern = r'[\t\t]'
        # import re
        for _element in _elements:
            if _element.find_element_by_xpath(_key_loc).text != '复查人':  # 隐患类型为现场处理时，不需要截取字符串
                _key_content = _element.find_element_by_xpath(_key_loc).text[:-1].replace('\t', '')
            else:
                _key_content = _element.find_element_by_xpath(_key_loc).text
            if '隐患处理' == _key_content:  # 去掉 ‘隐患处理’
                continue
            # _value_content = _element.find_element_by_xpath(_value_loc).text
            detail_dic[_key_content] = _element.find_element_by_xpath(_value_loc).text

        self.swipe_up()  # 滑动屏幕获取剩下的参数 👇
        _elements = self.get_elements('xpath', _xpath_loc)  # 查找三违详情相关的key和value
        for _element in _elements:
            if _element.find_element_by_xpath(_key_loc).text != '复查人':
                _key_content = _element.find_element_by_xpath(_key_loc).text[:-1].replace('\t', '')
            else:
                _key_content = _element.find_element_by_xpath(_key_loc).text
            if '隐患处理' == _key_content:
                continue
            # _value_content = _element.find_element_by_xpath(_value_loc).text
            detail_dic[_key_content] = _element.find_element_by_xpath(_value_loc).text

        return detail_dic

    def collect_detail_of_hidden_from_db(self, exam_date, exam_type, exam_desc, **kwargs):
        """
        数据库中隐患详情,根据指定的参数获取对用隐患详情
        :param exam_date: 检查时间
        :param exam_type: 隐患类型
        :param exam_desc: 隐患描述
        :param kwargs: 其他参数，比如责任单位/检查人。可为空
        :return:
        """
        details = {}  # 用于存放风险详情内容
        tmp_detail_list = []  # 存放临时变量
        tmp_limit_key_list = (
            '检查类型',
            '检查时间',
            '班次',
            '地点',
            '检查人',
            '责任单位',
            '责任人',
            '隐患类别',
            '隐患等级',
            '隐患类型',
            '限期日期',
            '问题描述')
        tmp_current_key_list = (
            '检查类型',
            '检查时间',
            '班次',
            '地点',
            '检查人',
            '责任单位',
            '责任人',
            '隐患类别',
            '隐患等级',
            '隐患类型',
            '复查人',
            '问题描述')

        from config import sql_constants
        if not kwargs:
            _tmp_deal_type = conn.get_info(sql_constants.get_deal_type_sql(exam_desc, exam_type, exam_date))
            tmp_detail = conn.get_infos(sql_constants.detail_of_hidden_sql(exam_desc, exam_type, exam_date))[0]  # 通过查询得到详情内容
        else:
            _tmp_deal_type = conn.get_info(sql_constants.get_deal_type_sql(
                hidden_desc=exam_desc, exam_type=exam_type, exam_date=exam_date, kwargs=kwargs[list(kwargs)[0]]))
            tmp_detail = conn.get_infos(sql_constants.detail_of_hidden_sql(
                hidden_desc=exam_desc, exam_type=exam_type, exam_date=exam_date, kwargs=kwargs[list(kwargs)[0]]))[0]  # 通过查询得到详情内容
        for _detail in tmp_detail:
            tmp_detail_list.append(_detail)

        if _tmp_deal_type == '1':
            """处理限期整改的隐患"""
            tmp_detail_list[1] = tmp_detail_list[1][:10]  # 处理检查时间, 截取年月日
            tmp_detail_list[-2] = tmp_detail_list[-2][:10]  # 处理限期日期, 截取年月日
            for _key in tmp_limit_key_list:
                details[_key] = tmp_detail_list[tmp_limit_key_list.index(_key)]

        if _tmp_deal_type == '2':
            """处理现场整改的隐患"""
            tmp_detail_list[1] = tmp_detail_list[1][:10]  # 处理检查时间, 截取年月日
            for _index in tmp_current_key_list:  # 将数据保存到details中
                details[_index] = tmp_detail_list[tmp_current_key_list.index(
                    _index)]

        return details

    def get_params_of_hidden(self, tag='2'):
        """获取隐患时间/检查类型/隐患描述/责任单位字段值
            1表示不获取unit的值，可在隐患录入时使用
            2表示获取unit的值
        """
        global tmp_elements
        if tag == '2':
            tmp_elements = self.get_elements('xpath', "//*[@resource-id='com.universal:id/list_view']/android.widget.RelativeLayout")
            if len(tmp_elements) > 0:
                _index = random.randint(0, len(tmp_elements) - 1)
                _date = tmp_elements[_index].find_element_by_id('com.universal:id/text_date').text
                _type = tmp_elements[_index].find_element_by_id('com.universal:id/text_check').text
                _desc = tmp_elements[_index].find_element_by_id('com.universal:id/text_describe').text
                _unit = tmp_elements[_index].find_element_by_id('com.universal:id/text_unit').text
                return _date, _type, _desc, _unit
            else:
                logger.warning('no hidden config')
        else:
            tmp_elements = self.get_elements('xpath', "//*[@resource-id='com.universal:id/recyclerView']/android.widget.RelativeLayout")
            if len(tmp_elements) > 0:
                _index = random.randint(0, len(tmp_elements) - 1)
                _date = tmp_elements[_index].find_element_by_id('com.universal:id/text_date').text
                _type = tmp_elements[_index].find_element_by_id('com.universal:id/text_check').text
                _desc = tmp_elements[_index].find_element_by_id('com.universal:id/text_describe').text
                return _date, _type, _desc
            else:
                logger.warning('no hidden config')

    def text_zh(self, chars_length=None):
        """
        使用faker伪造指定长度的字符串
        :param chars_length: 字串长度
        :return:
        """
        fake = Faker('zh_CN')
        if chars_length is not None:
            _s = fake.text().replace('\n', '')
            while len(_s) != chars_length:
                _s = _s + fake.text().replace('\n', '')
                if len(_s) > chars_length:
                    break
            return _s[:chars_length]
        else:
            return fake.text()

    def collect_address_name(self):
        address_names = []
        vio_tmp_elements = self.driver.get_elements(by='xpath', value="//*[@resource-id='com.universal:id/recyclerView']/android.widget.LinearLayout")
        for element in vio_tmp_elements:
            pattern = r'[【|】]'
            _tmp_str = re.split(pattern, element.find_element_by_id('com.universal:id/text_risk_point_name').text)[1]  # 👈获取危险源名称
            address_names.append(_tmp_str)
        return address_names
