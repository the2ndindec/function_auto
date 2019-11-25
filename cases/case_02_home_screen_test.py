# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_02_home_screen_test.py
date: 2019/11/25 14:37
Desc:
"""
import pytest

from common.init_operate import BaseTest


class TestHome(BaseTest):

    @pytest.mark.skip('to fix')
    def test_01_synchronize(self):
        self.home_screen.sync_data()
        # assert self.home_screen.get_toast('同步完成') is True
        self.driver.assert_true(self.home_screen.get_toast('同步完成'))
