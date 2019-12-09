## 工程依赖及版本号
1. PyMySQL==0.9.3
2. pytest==5.2.4
3. allure_python_commons==2.8.6
4. selenium==3.141.0
5. Appium_Python_Client==0.48
#### 简单介绍下用法
* 运行前请添加测试包、设备信息、服务信息配置到./config/server_config.ini文件,数据库信息配置到./config/db.ini文件
~~~
server_config.ini文件-----------------------------------
[desired_caps]
platformName='Android'
deviceName='333a0a4a'
platformVersion='7.1'
appPackage='com.universal'
appActivity='.activity.SplashActivity'
[driver]
driverIp='http://127.0.0.1:4723/wd/hub'  #appium服务地址
[server]
server='192.168.3.200:8080/sdzk'  #程序运行地址
db.ini文件----------------------------------------------
[db]
db_host=192.168.3.200
db_post=3306
db_user=root
db_password=admin
db_datatable=sdzk-mine
~~~
👉 运行时需确认手机已连接，appium服务已开启
* 脚本中涉及到的参数可先配置在./config/param.xlsx中。hidden 页配置隐患相关参数信息，vio页配置三违相关参数信息
👉 确保参数存在系统中