# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_03_vio_add_scerrn_test.py
date: 2019/11/25 16:41
Desc: 三违录入
"""
import pytest

from common.init_operate import BaseTest
from pages.home_screen import HomeScreen


class TestVioAdd(BaseTest):

    # @pytest.mark.smoketest
    def test_01_add_vio_success(self):
        """三违数据上报"""
        self.home_screen.select_module(HomeScreen.three_vio_add)
        self.vio_add_screen.choose_vio_date('2019-11-26')
        self.vio_add_screen.choose_vio_address("南翼集中煤仓")
        self.vio_add_screen.choose_vio_people('马勇')
        self.vio_add_screen.choose_vio_level('一般B级')
        self.vio_add_screen.choose_vio_check_unit('综采一区')
        self.vio_add_screen.type_vio_desc('三违事实描述内容')
        self.vio_add_screen.choose_vio_shift('早班')
        self.vio_add_screen.choose_vio_unit('综采二区')
        self.vio_add_screen.choose_vio_category('违规作业')
        self.vio_add_screen.choose_vio_qualitative('一般三违')
        self.vio_add_screen.choose_stop_person('马勇')
        self.driver.swipe_up()
        self.vio_add_screen.submit_vio()
        # 以上为录入三违相关数据 ↑，之后返回主界面，上报三违数据 ↓
        self.driver.click_back()
        self.home_screen.select_module(HomeScreen.vio_upload)
        # todo add assertion
