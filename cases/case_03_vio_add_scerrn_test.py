# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_03_vio_add_scerrn_test.py
date: 2019/11/25 16:41
Desc: 三违录入
"""
from common.init_operate import BaseTest
from pages.home_screen import HomeScreen


class TestVioAdd(BaseTest):

    def test_01_login_success(self):
        self.home_screen.select_module(HomeScreen.three_vio_add)
        self.vio_add_screen.choose_vio_date('2019-11-11')