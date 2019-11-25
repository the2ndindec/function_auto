# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: base_page.py
date: 2019/11/25 13:11
Desc: page基类
"""


class BasePage:
    def __init__(self, driver):
        self.driver = driver
