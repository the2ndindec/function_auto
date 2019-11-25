# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: pytest_run.py
date: 2019/11/25 14:11
Desc:
"""
import os

import pytest

curPath = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    # remove_old_file(init_env('/report/json/'))
    # 运行测试脚本
    pytest.main(['--alluredir', './report/xml', '-v', '-s', "./cases"])
    # # 生成测试报告
    os.popen("allure generate ./report/xml/ -o ./report/html --clean")

