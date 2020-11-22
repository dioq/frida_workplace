# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.wuba.wchat.api.bean.CallbackHolder");//获取到类
        util.getObj.overload().implementation = function(){
            console.log("------------ getObj ------------");
            var ret = this.getObj();
            console.log("ret : " + ret);
            return ret;
        }
        util.setObj.overload("java.lang.Object").implementation = function(p1){
            console.log("------------ setObj ------------");
            console.log("ret : " + ret);
            this.setObj(p1);
        }
        util.getCallback.overload().implementation = function(){
            console.log("------------  getCallback ------------");
            var ret = this.getCallback();
            console.log("ret : " + ret);
            return ret;
        }
        util.setCallback.overload("java.lang.Object").implementation = function(p1){
            console.log("------------  setCallback ------------");
            this.setCallback(p1);
            console.log("p1 : " + p1);
        }
        util.getErrorInfo.overload().implementation = function(){
            console.log("------------  getErrorInfo ------------");
            var ret = this.getErrorInfo();
            console.log("ret : " + ret);
            return ret;
        }
        util.setErrorInfo.overload("java.lang.Object").implementation = function(p1){
            console.log("------------  setErrorInfo ------------");
            this.setErrorInfo(p1);
            console.log("p1 : " + p1);
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
