# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.fenzotech.jimu.login.bean.RegisterRequest");//获取到类
        util.getJpush_token.overload().implementation = function(){
            //打印堆栈
            console.log("hook getJpush_token ...");
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getJpush_token();
            console.log("getJpush_token --->　ret : " + ret);
            return ret;
        }
        util.setJpush_token.overload("java.lang.String").implementation = function(p1){
            //打印堆栈
            console.log("hook setJpush_token ...");
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            this.setJpush_token(p1);
            console.log("setJpush_token ---> p1 : " + p1);
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
