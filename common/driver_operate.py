# -*- coding: utf-8 -*-
"""
version: 1.0
author:
file name: driver_operate.py
date: 2019/11/25 13:45
Desc: driver配置
"""
from appium import webdriver


class DriverConfig:
    """初始化driver"""
    def __new__(cls, *args, **kwargs):
        """使用单例模式将类型设置为运行时只有一个实例"""
        try:
            # hasattr()函数功能用来检测对象object中是否含有名为**的属性,如果有就返回True，没有就返回False
            if not hasattr(cls, '_instance'):
                orig = super(DriverConfig, cls)
                desired_caps = {
                    'platformName': 'Android',  # 平台
                    'platformVersion': '7.1',   # 系统版本
                    'appPackage': 'com.universal',  # APK包名
                    'appActivity': '.activity.SplashActivity',  # 被测程序启动时的Activity
                    'unicodeKeyboard': 'true',  # 是否支持unicode的键盘。如果需要输入中文，要设置为“true”
                    'resetKeyboard': 'true',    # 是否在测试结束后将键盘重置为系统默认的输入法。
                    'newCommandTimeout': '120',  # Appium服务器待appium客户端发送新消息的时间。默认为60秒
                    'deviceName': '333a0a4a',   # 手机ID
                    'noReset': True,  # true:不重新安装APP，false:重新安装app.每次启动APP不清除之前的状态
                    'automationName': 'Uiautomator2'    # 用于获取toast
                }
                # desired_caps['app'] = '/xxxxx.apk'  #
                # 指向.apk文件，如果设置appPackage和appActivity，那么这项会被忽略

                cls._instance = orig.__new__(cls)
                cls._instance.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
            return cls._instance
        except Exception as msg:
            raise msg

    # def get_driver(self):
    # 此方法会导致每执行完一个py文件后重新启动一次driver
    #     try:
    #         self.desired_caps = {}
    #         self.desired_caps['platformName'] = 'Android'  # 平台
    #         self.desired_caps['platformVersion'] = '7.1'  # 系统版本
    #         # self.desired_caps['app'] = 'E:/xxxxx.apk'   # 指向.apk文件，如果设置appPackage和appActivity，那么这项会被忽略
    #         self.desired_caps['appPackage'] = 'com.universal'  # APK包名
    #         self.desired_caps['appActivity'] = '.activity.SplashActivity'  # 被测程序启动时的Activity
    #         self.desired_caps['unicodeKeyboard'] = 'true'  # 是否支持unicode的键盘。如果需要输入中文，要设置为“true”
    #         self.desired_caps['resetKeyboard'] = 'true'  # 是否在测试结束后将键盘重置为系统默认的输入法。
    #         self.desired_caps['newCommandTimeout'] = '120'  # Appium服务器待appium客户端发送新消息的时间。默认为60秒
    #         self.desired_caps['deviceName'] = '333a0a4a'  # 手机ID
    #         self.desired_caps['noReset'] = True  # true:不重新安装APP，false:重新安装app
    #         self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.desired_caps)
    #         return self.driver
    #     except Exception as e:
    #         raise e


class DriverClient(DriverConfig):
    def get_driver(self):
        return self.driver


if __name__ == '__main__':
    d = DriverClient()
    d.get_driver()
