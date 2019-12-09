# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_01_login_screen_test.py
date: 2019/11/25 11:21
Desc:
"""
import time

import pytest

from common import read_config
from common.init_operate import BaseTest


class TestLogin(BaseTest):
    readeConfigObj = read_config.ReadConfig("\\config\\server_config.ini")
    @pytest.mark.smoketest
    def test_01_login_success(self):
        # self.login_screen.permission()
        # 执行测试脚本时，取消以下三行注释 👇
        self.login_screen.server_opera(self.readeConfigObj.get_config('server', 'server'))
        self.login_screen.input_username('admin')
        self.login_screen.input_password('123456')
        self.login_screen.click_loginbtn()
        time.sleep(1)
        self.driver.assert_equal(self.login_screen.login_success(), '主页')

