# -*- coding: utf-8 -*-
import frida, sys

# HOOK Url初始化方法
jscode = """
if(Java.available){
    Java.perform(function(){
        var Classz = Java.use("com.fenzotech.jimu.login.activity.LoginActivity");
        Classz.a.overload("com.fenzotech.jimu.login.bean.LoginResponse").implementation=function(param1){
            console.log("111 ------------- a ----------------");
            //打印堆栈
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            console.log("param1 : \\n" + param1);
            this.a(param1);
        }
        Classz.a.overload("com.fenzotech.jimu.login.bean.LoginResponse","java.lang.String","java.lang.String","java.lang.String").implementation=function(param1,p2,p3,p4){
            console.log("22222 ------------- a ----------------");
            //打印堆栈
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            console.log("p1 : " + param1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            this.a(param1,p2,p3,p4);
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
