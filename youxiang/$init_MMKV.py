# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 21:55:28 2020

@author: Dio
"""

import frida, sys

#$init_MMKV
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.tencent.mmkv.MMKV");//获取到类
        util.$init.overload("long").implementation = function(param){
            console.log("param : " + param);
            var result = this.$init(param);
            //console.log("result : " + result);
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