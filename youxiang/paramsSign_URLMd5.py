# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:24:42 2020

@author: Dio
"""

import frida, sys

#paramsSign_URLMd5
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.soyoung.library_utils.encrypt.URLMd5");//获取到类
        util.md5_32.overload("java.lang.String").implementation = function(param){
            console.log("param : " + param);
            var newParam = "_time=1591967587&app_id=2&cityId=0&device_id=207435000&device_model=google-google Pixel 2&device_os_version=5.1.1&key=faefb0f142f6e9079036f0b2a788e916&lat=39.916295&lng=116.410344&login_name=17683927317&lver=7.52.1&password=1qaz2wsx&pinyin=soyoung&request_id=da015dc05acc28805f53e75a9b366126&sdk_version=22&sm_device_id=202006111607080036e9a302acf4ac8dd68727748c9a39015589015d57ec2b&sys=2&uid=0&uuid=697872c21df50562&vistor_uid=0&xy_device_token=4b8d9f77b14695ad750d49c9ee1a0d0eb3";
            var result = this.md5_32(newParam);
            console.log("result : " + result);
            return result;
        }
    });
}
"""

def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)

# 查找USB设备并附加到目标进程
session = frida.get_usb_device().attach('com.youxiang.soyoungapp')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()