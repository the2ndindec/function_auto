# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: init_operate.py
date: 2019/11/25 14:06
Desc:
"""
from common import driver_operate
from common.base_operate import BaseOperate
from pages.hidden_danger_screen import HiddenDangerScreen
from pages.home_screen import HomeScreen
from pages.login_screen import LoginScreen
from pages.major_risk_screen import MajorRiskScreen
from pages.address_screen import AddressScreen
from pages.pending_rectify_screen import PendingRectifyScreen
from pages.pending_review_screen import PendingReviewScreen
from pages.vio_add_screen import VioAddScreen


class BaseTest:

    def setup_class(self):
        driver_config = driver_operate.DriverClient()
        self.driver = BaseOperate(driver_config.get_driver())
        self.login_screen = LoginScreen(self.driver)
        self.home_screen = HomeScreen(self.driver)
        self.vio_add_screen = VioAddScreen(self.driver)
        self.major_screen = MajorRiskScreen(self.driver)
        self.address_point_screen = AddressScreen(self.driver)
        self.hidden_screen = HiddenDangerScreen(self.driver)
        self.pending_rectify_screen = PendingRectifyScreen(self.driver)
        self.pending_review_screen = PendingReviewScreen(self.driver)

    def setup(self):
        pass

    def teardown(self):
        # self.driver.quit()
        pass
