# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:08:29 2020

@author: Dio
"""

import frida, sys

# HOOK 打印所有的类及方法
jscode = """
if(Java.available){
    Java.perform(function(){
    
            

    });
}
"""


def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)


# 查找USB设备并附加到目标进程
session = frida.get_usb_device().attach('com.vmos.pro')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()

