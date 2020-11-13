# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.wuba.wchat.api.internal.UniversalToolsImp");//获取到类
        util.a.overload("android.os.Message").implementation = function(p1){
            console.log("Hook Start...");
            console.log("p1 : " + p1);
            this.a(p1);
        }
        util.a.overload("java.lang.String","org.json.JSONObject","com.wuba.wchat.api.Define$RequestSessionCb").implementation = function(p1,p2,p3){
            console.log("Hook Start 222 ...");
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            this.a(p1,p2,p3);
        }
        util.a.overload("java.lang.String","java.util.HashMap","com.wuba.wchat.api.Define$RequestSessionCb").implementation = function(p1,map,p3){
            console.log("Hook Start 333 ...");
            console.log("p1 : " + p1);
            console.log("p2 : " + map);
            var result = "";
            var keyset = map.keySet();
            var it = keyset.iterator();
            while(it.hasNext()){
                var keystr = it.next().toString();
                var valuestr = map.get(keystr).toString();
                result += valuestr;
            }
            console.log("result : " + result);
            console.log("p3 : " + p3);
            this.a(p1,map,p3);
        }
        util.requestSessionByBody.overload('long', 'java.lang.String', 'boolean', 'java.lang.String', 'java.lang.Object').implementation = function(p1,p2,p3,p4,p5){
            console.log("Hook Start 444 ...");
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            console.log("p5 : " + p5);
            this.requestSessionByBody(p1,p2,p3,p4,p5);
        }
        util.requestSessionByBodyWithBangBang.implementation = function(p1,p2,p3,p4,p5,p6,p7,p8){
            console.log("requestSessionByBodyWithBangBang 444__222 ...");
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            console.log("p5 : " + p5);
            console.log("p6 : " + p6);
            console.log("p7 : " + p7);
            console.log("p8 : " + p8);
            this.requestSessionByBodyWithBangBang(p1,p2,p3,p4,p5,p6,p7,p8);
        }
        util.checkUserHasMsgAsyncN.implementation = function(p1,p2,p3,p4){
            console.log("checkUserHasMsgAsyncN ...");
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            this.checkUserHasMsgAsyncN(p1,p2,p3,p4);
        }
        util.globalSearchN.implementation = function(p1,p2,p3,p4,p5){
            console.log("globalSearchN ...");
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            console.log("p5 : " + p5);
            this.globalSearchN(p1,p2,p3,p4,p5);
        }
        util.mergeUserAsyncN.implementation = function(p1,p2,p3,p4){
            console.log("mergeUserAsyncN ...");
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            this.mergeUserAsyncN(p1,p2,p3,p4);
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
