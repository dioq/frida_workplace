# -*- coding: utf-8 -*-

import frida
import sys

jscode = """
if(Java.available){
    Java.perform(function(){
        //hook动态函数，找到instance实例，从实例调用函数方法
        Java.choose("com.yestae.yigou.customview.SubScribingView",{
            onMatch:function(instance){
                console.log("changeState ---->");
                instance.changeState(0x0350);
            },onComplete:function(){}
        })
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
