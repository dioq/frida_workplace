# -*- coding: utf-8 -*-
import frida, sys
# .overload("android.net.Uri","[java.lang.String","java.lang.String","[java.lang.String","java.lang.String")
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.wuba.commons.utils.PublicPreferencesProvider");//获取到类
        util.query.implementation = function(p1,p2,p3,p4,p5){
            console.log("--------- start ----------");
            var ret = this.query(p1,p2,p3,p4,p5);
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            //for (var i = 0; i < p2.length; i++) {
            //    console.log(i + "  :  " + p2[i]);
            //}
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            //for (var i = 0; i < p4.length; i++) {
            //    console.log(i + "  :  " + p4[i]);
            //}
            console.log("p5 : " + p5);
            console.log("ret : " + ret);
            return ret;
            console.log("--------- end ----------");
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
