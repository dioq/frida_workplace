# -*- coding: utf-8 -*-

import frida, sys

#HOOK普通方法 (除了不指定参数类型外,跟hook Overload重载方法写法一样)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.yunbao.common.http.CommonHttpUtil");//获取到类
        util.circleAds.implementation = function(param1){
            console.log("Hook Start...");
            console.log("p1 : " + param1);
            this.circleAds(param1);
            this.circleAds(param1);
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
session = frida.get_usb_device().attach('com.qzdsp.tiktok')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()