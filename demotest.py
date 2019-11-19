# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: demotest.py
date: 2019/11/19 11:30
Desc:
"""
import os

from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

desired_caps = {
            'platformName': 'Android',
            'platformVersion': '7.1.2',
            'deviceName': '333a0a4a',
            # 'newCommandTimeout': 240,
            # "udid": "U8ENW18115006649",
            "appActivity": ".activity.SplashActivity",
            "appPackage": "com.universal"
        }
driver = webdriver.Remote(
            'http://localhost:4723/wd/hub', desired_caps)
