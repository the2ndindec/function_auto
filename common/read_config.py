# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: read_config.py
date: 2019/11/25 13:04
Desc:
"""
import codecs
import configparser
import os


class ReadConfig:
    def __init__(self, filename):
        pro_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = pro_dir + filename
        fd = open(config_path, encoding='UTF-8')
        data = fd.read()

        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(config_path, "w")
            file.write(data)
            file.close()
        fd.close()

        self.conf = configparser.ConfigParser()
        self.conf.read(config_path, encoding='UTF-8')

    def get_config(self, section, name):
        value = self.conf.get(section, name)
        return value

    def get_sections(self):
        value = self.conf.sections()
        return value

    def get_items(self, section):
        value = self.conf.items(section)
        return value
