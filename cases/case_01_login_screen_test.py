# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_01_login_screen_test.py
date: 2019/11/25 11:21
Desc:
"""
import time
import unittest

from common.init_operate import BaseTest


class TestLogin(BaseTest):

    def test_01_login_success(self):
        # self.login_screen.permission()
        self.login_screen.server_opera('192.168.3.113:8081/sdzk-mine')
        self.login_screen.input_username('admin')
        self.login_screen.input_password('123456')
        self.login_screen.click_loginbtn()
        time.sleep(1)
        # assert self.login_screen.login_success() == '主页'
        self.driver.assert_equal(self.login_screen.login_success(), '主页')

