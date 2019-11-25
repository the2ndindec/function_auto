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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_xpath(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
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
        except:
            print("not find element")

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
                elements = self.driver.find_element_bys_xpath(find_name)
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
        except:
            print("not find element")

    def click_element(self, value):
        """封装点击"""
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
        element = self.get_element(value)
        return element.is_displayed()

    def is_exist_current(self, text):
        """通过获取所有元素来判断当前text是否存在"""
        all_element = self.driver.page_source
        return text in all_element

    def is_toast_exist(self, toast_text):
        """验证toast是否出现"""
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % toast_text)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(toast_loc))
            return True
        except:
            return False

    def get_screen_shot(self, case_name):
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

    def deal_date_piker(self, date_str):
        """处理日期"""
        _year = str(date_str).split('-')[0]
        _month = str(date_str).split('-')[1]
        _day = str(date_str).split('-')[2]
        _number_pickers = self.get_elements('class_name', 'android.widget.NumberPicker')
        # year
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

        # month
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

        # day
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
