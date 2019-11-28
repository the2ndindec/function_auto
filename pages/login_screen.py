# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: login_screen.py
date: 2019/11/25 13:16
Desc: 登录页元素配置
"""
import allure

from common import read_config
from pages.base_page import BasePage


class LoginScreen(BasePage):
    readeConfigObj = read_config.ReadConfig("\\data\\base_xpath.ini")
    # loginCenterBtn = readeConfigObj.get_config('login', 'loginCenter_btn')
    usernameText = readeConfigObj.get_config('login', 'username_text')
    passwordText = readeConfigObj.get_config('login', 'password_text')
    loginBtn = readeConfigObj.get_config('login', 'login_btn')
    loginSuccess = readeConfigObj.get_config('login', 'main_assets')
    permission_continue_btn = readeConfigObj.get_config('login', 'permission_continue_btn')
    serverOpera = readeConfigObj.get_config('login', 'serverOpera')
    server_text = readeConfigObj.get_config('login', 'server_text')
    server_submit = readeConfigObj.get_config('login', 'server_submit')
    # driver = base_page.BasePage.get_driver()

    def server_opera(self, server):
        """配置服务"""
        with allure.step('配置服务地址：' + server):
            self.driver.click_element(self.serverOpera)
            self.driver.input_text(self.server_text, server)
            self.driver.click_element(self.server_submit)

    def permission(self):
        self.driver.click_element(self.permission_continue_btn)
        self.driver.click_element(self.permission_continue_btn)
        self.driver.click_element(self.permission_continue_btn)

    def input_username(self, username):
        with allure.step('使用：' + username):
            self.driver.input_text(self.usernameText, username)

    def input_password(self, password):
        self.driver.input_text(self.passwordText, password)

    def click_loginbtn(self):
        self.driver.click_element(self.loginBtn)

    # 验证是否登录成功
    def login_success(self):
        # self.driver.find_element_by_name(self.loginSuccess).text
        _text = self.driver.get_element_text(self.loginSuccess)
        return _text
