# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: case_02_home_screen_test.py
date: 2019/11/25 14:37
Desc:
"""
import allure
import pytest

from common.init_operate import BaseTest


class TestHome(BaseTest):

    @pytest.mark.skip('unfinished')
    def test_01_synchronize(self):
        self.home_screen.sync_data()
        # assert self.home_screen.get_toast('同步完成') is True
        self.driver.assert_true(self.home_screen.get_toast('同步完成'))

    # @pytest.mark.smoketest
    @pytest.mark.dependency(depends=["ahc"])
    def test_02_upload_risk_data(self):
        # fixme 验证失败
        _assert_text = self.driver.get_element_text(self.home_screen.risk_upload)
        with allure.step('同步隐患数据'):
            self.driver.click_element(self.home_screen.risk_upload)
        _assert_text_after = self.driver.get_element_text(self.home_screen.risk_upload)
        self.driver.assert_not_equal(_assert_text, _assert_text_after)
