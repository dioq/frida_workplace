# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:07:48 2020

@author: Dio
"""

import frida, sys


jscode = """
if(Java.available){
    Java.perform(function(){
        var Singleton = Java.use("com.soyoung.library_network.base_api.AppApiHelper");//获取到类
        var util = Singleton.getInstance();//获取到类
        util.post.overload("java.lang.String","java.util.HashMap",'boolean').implementation = function(param,p2,p3){
            var result = util.post(param,p2,p3);
            console.log("param : " + param);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            var commonParasm = util.getCommonParasm(p2);
            console.log("commonParasm : " + commonParasm);
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