# -*- coding: utf-8 -*-
import frida, sys

# HOOK OkHttp的请求request
jscode = """
if(Java.available){
    Java.perform(function () {
        var OkHttpClient = Java.use("okhttp3.OkHttpClient");
        var Gson = Java.use("com.google.gson.Gson");
        OkHttpClient.newCall.overload("okhttp3.Request").implementation = function (request) {
            var gson = Gson.$new();
            var result_json = gson.toJson(request);
            console.log("result_json : " + result_json);
            var result = this.newCall(request);
            //console.log("result : "+request.toString());
            return result;
        };
    });
}
"""


def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)


# 查找USB设备并附加到目标进程
session = frida.get_usb_device().attach('com.my.network')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
