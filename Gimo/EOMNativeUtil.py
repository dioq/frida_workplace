# -*- coding: utf-8 -*-
import frida
import sys

# HOOK普通方法 (除了不指定参数类型外,跟hook Overload重载方法写法一样)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.eom.tools.EOMNativeUtil");//获取到类
        util.decrypt.overload("java.lang.String","java.lang.String").implementation = function(param1, param2){
            //打印堆栈
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.decrypt(param1, param2);
            console.log("decrypt --> p1 : \\n" + param1);
            console.log("decrypt --> p2 : \\n" + param2);
            console.log("decrypt --> ret : \\n" + ret);
            return ret;
        }
        util.encrypt.overload("java.lang.String","java.lang.String").implementation = function(param1, param2){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.encrypt(param1, param2);
            console.log("p1 : " + param1);
            console.log("p2 : " + param2);
            console.log("ret : " + ret);
            return ret;
        }
        util.getAliDeviceId.overload("java.lang.String").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getAliDeviceId(param1);
            console.log("p1 : " + param1);
            console.log("p2 : " + param2);
            console.log("ret : " + ret);
            return ret;
        }
        util.decryptHXPassword.overload("java.lang.String").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.decryptHXPassword(param1);
            console.log("decryptHXPassword --> p1 : \\n" + param1);
            console.log("decryptHXPassword --> ret : \\n" + ret);
            return ret;
        }
        util.getAc.overload("long").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getAc(param1);
            console.log("p1 : " + param1);
            console.log("ret : " + ret);
            return ret;
        }
        util.getGSHeader.overload("java.lang.String","java.lang.String","java.lang.String","long").implementation = function(p1,p2,p3,p4){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getGSHeader(p1,p2,p3,p4);
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            console.log("ret : " + ret);
            return ret;
        }
        util.getHXUserName.overload("boolean","long").implementation = function(p1,p2){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getHXUserName(p1,p2);
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("ret : " + ret);
            return ret;
        }
        util.getSign.overload("java.lang.String").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getSign(param1);
            console.log("p1 : " + param1);
            console.log("ret : " + ret);
            return ret;
        }
        util.getSignature.overload("java.lang.String").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getSignature(param1);
            console.log("p1 : " + param1);
            console.log("ret : " + ret);
            return ret;
        }
        util.getUUID.overload("java.lang.String").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getUUID(param1);
            console.log("p1 : " + param1);
            console.log("ret : " + ret);
            return ret;
        }
        util.getPassword.overload("java.lang.String").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getPassword(param1);
            console.log("getPassword --> p1 : " + param1);
            console.log("getPassword --> ret : " + ret);
            return ret;
        }
        util.getMD5.overload("java.lang.String").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getMD5(param1);
            console.log("getMD5 --> p1 : " + param1);
            console.log("getMD5 --> ret : " + ret);
            return ret;
        }
        util.getUUID.overload("java.lang.String").implementation = function(param1){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            var ret = this.getUUID(param1);
            console.log("getUUID --> p1 : " + param1);
            console.log("getUUID --> ret : " + ret);
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
