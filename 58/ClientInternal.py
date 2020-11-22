# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.wuba.wchat.api.internal.ClientInternal");//获取到类
        util.setServerLevel.overload("int").implementation = function(p1){
            console.log("p1 : " + p1);
            this.setServerLevel(p1);
        }
        util.regRegistedUserInfoChangedCb.overload("long","java.lang.Object").implementation = function(p1,p2){
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            this.regRegistedUserInfoChangedCb(p1,p2);
        }
        util.b.overload("android.os.Message").implementation = function(p1){
            console.log("-------- b ----------");
            console.log("p1 : " + p1);
            this.b(p1);
        }
        
        var a = Java.use("com.wuba.wchat.api.internal.ClientInternal$a");
        a.handleMessage.overload("android.os.Message").implementation = function(p1){
            console.log("-------- ClientInternal$a ----------");
            console.log("p1 : " + p1);
            this.handleMessage(p1);
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
session = frida.get_usb_device().attach('com.wuba')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
