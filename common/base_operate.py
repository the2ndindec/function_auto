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
            
    CONTROL_LOC = "class>=android.widget.LinearLayout"  # 弹窗

    def choose_attr_value(self, attr, attr_value):
        """选择属性参数"""
        self.click_element(attr)
        self.choose_param(attr_value, self.CONTROL_LOC)

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
