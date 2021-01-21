# -*- coding: utf-8 -*-

import frida
import sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.yestae.yigou.YiGouFragment");//获取到类
        util.yigou_home_shoppcart.implementation = function(){
            console.log("---------- go here ---------- ");
            this.yigou_home_shoppcart();
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
session = frida.get_usb_device().attach('com.uustock.dayi')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
