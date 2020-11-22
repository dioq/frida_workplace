# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.wuba.login.LoginHandle");//获取到类
        var Gson = Java.use("com.google.gson.Gson");
        util.commandCall.overload('android.content.Context', 'com.wuba.walle.Request', 'com.wuba.walle.Response').implementation = function(p1,p2,p3){
            this.commandCall(p1,p2,p3);
            console.log("p2 : " + p2);
            var gson = Gson.$new();
            var request_json = gson.toJson(p2);
            console.log("request_json : " + request_json);
            console.log("p3 : " + p3);
            var response_json = gson.toJson(p3);
            console.log("response_json : " + response_json);
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
