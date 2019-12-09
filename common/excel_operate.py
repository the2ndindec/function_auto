# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: excel_operate.py
date: 2019/12/5 11:01
Desc: excel读取
"""
import os
import random

import xlrd

# path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '../config/')


def read_excel(tag, *args):
    """
    读取excel数据
    :param tag: 表示隐患或者三违
    :param args: 取第几行数据，表示 args+1行数据
    :return:
    """

    global rows_num, cols_num, hidden_sheet, vio_sheet, workbook

    workbook = xlrd.open_workbook(os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/config/param.xlsx'))   # 打开excel文件

    if tag == 'hidden':  # 隐患
        hidden_sheet = workbook.sheet_by_name('hidden')
        rows_num = hidden_sheet.nrows  # 获取行数
        _dict = {}
        _list = hidden_sheet.row_values(0)  # 获取第一行的值，作为key来使用
        if args:
            # 如果指定行的序号大于总行数，则随机获取当前sheet中某行的数据
            if args[0] > rows_num:
                raise IndexError('list index out of range')
            else:
                row = hidden_sheet.row_values(random.randint(1, rows_num - 1))
            if row:
                for index, item in enumerate(_list):
                    _dict[item] = row[index]
        else:
            for curr_row in range(1, rows_num):  # 遍历所有行 fixme 只会读取到最后一行数据
                row = hidden_sheet.row_values(curr_row)
                if row:
                    for index, item in enumerate(_list):
                        _dict[item] = row[index]
        return _dict

    if tag == 'vio':  # 三违
        vio_sheet = workbook.sheet_by_name('vio')
        rows_num = vio_sheet.nrows
        cols_num = vio_sheet.ncols
        _dict = {}  # 存放三违参数
        _list = vio_sheet.row_values(0)  # 获取第一行的值，作为key来使用
        if args:
            # 如果指定行的序号大于总行数，则随机获取当前sheet中某行的数据
            if args[0] > rows_num:
                raise IndexError('list index out of range')
            else:
                row = vio_sheet.row_values(random.randint(1, rows_num - 1))
            if row:
                for index, item in enumerate(_list):
                    _dict[item] = row[index]
        else:
            for curr_row in range(1, rows_num - 1):  # 遍历所有行 fixme 只会读取到最后一行数据
                row = vio_sheet.row_values(curr_row)
                if row:
                    for index, item in enumerate(_list):
                        _dict[item] = row[index]
        return _dict


if __name__ == '__main__':
    print(read_excel('vio', 5))
