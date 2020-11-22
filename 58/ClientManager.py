# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var Singleton = Java.use("com.common.gmacs.core.ClientManager");//获取到类
        var util = Singleton.getInstance();//调用单例方法初始化一个对象
        util.getUserId.overload().implementation = function(){
            console.log("------------ getUserId ------------");
            var result = this.getUserId();
            console.log("getUserId result : \\n" + result);
            return result;
        }
        util.getSource.overload().implementation = function(){
            console.log("------------ getSource ------------");
            var result = this.getSource();
            console.log("getSource result : \\n" + result);
            return result;
        }
        util.pushReceivedMsg.overload("java.lang.String","int","java.lang.String","int","long").implementation = function(p1,p2,p3,p4,p5){
            console.log("------------ pushReceivedMsg ------------");
            var param = "p1 : " + p1 + "\\np2 : " + p2 + "\\np3 :" + p3 + "\\np4: " + p4 + "\\np5: " + p5;
            console.log(param);
            var result = this.pushReceivedMsg(p1,p2,p3,p4,p5);
            console.log("pushReceivedMsg result : \\n" + result);
            return result;
        }
        util.setSmartId.overload("java.lang.String").implementation = function(p1){
            console.log("------------ setSmartId ------------");
            var param = "p1 : " + p1;
            console.log("setSmartId p1 : \\n" + param);
            this.setSmartId(p1);
        }
        util.isSelf.overload("java.lang.String","int").implementation = function(p1,p2){
            console.log("------------ isSelf ------------");
            var param = "p1 : " + p1 + "\\np2 : " + p2;
            console.log("isSelf " + param);
            this.isSelf(p1,p2);
        }
        util.getServerEnvi.overload().implementation = function(){
            console.log("------------ getServerEnvi ------------");
            var ret = this.getServerEnvi();
            console.log("ret : " + ret);
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
