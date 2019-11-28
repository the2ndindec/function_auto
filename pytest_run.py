# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: pytest_run.py
date: 2019/11/25 14:11
Desc:
"""
import os
import platform

import pytest

curPath = os.path.abspath(os.path.dirname(__file__))


def init_env(addr):
    """初始化文件夹"""
    base_addr = os.path.dirname(os.path.abspath(__file__))
    full_addr = base_addr + addr
    if 'Windows' in platform.system():
        addr = full_addr.replace('/', '\\')
        return addr
    return full_addr


def remove_old_file(path):
    """删除文件夹下的文件"""
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)


if __name__ == '__main__':
    remove_old_file(init_env('/report/xml'))
    remove_old_file(init_env('/screenshots'))
    # 运行测试脚本
    pytest.main(['--alluredir', './report/xml', '-v', '-s', "./cases", '-m', 'smoketest'])
    # # 生成测试报告
    os.popen("allure generate ./report/xml/ -o ./report/html --clean")

