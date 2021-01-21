# -*- coding: utf-8 -*-
import frida
import sys

# HOOK普通方法 (除了不指定参数类型外,跟hook Overload重载方法写法一样)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("okhttp3.a.e");//获取到类
        util.a.overload("java.lang.String","java.lang.String").implementation = function(p1,p2){
            console.log("Hook Start...");
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            /*
            if (param1 === "http.proxyHost" || param1 === "http.proxyPort" || param1 === "https.proxyHost" || param1 === "https.proxyPort"){
                return null;
            }
            */
            var ret = this.a(p1,p2);
            console.log("ret : " + ret);
            return ret;
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
session = frida.get_usb_device().attach('com.fenzotech.jimu')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
