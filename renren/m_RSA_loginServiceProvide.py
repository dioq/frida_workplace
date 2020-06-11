# -*- coding: utf-8 -*-

import frida, sys

#HOOK 静态方法
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.renren.mobile.android.service.ServiceProvider");//获取到类
        util.m_RSA_login.overload("java.lang.String","java.lang.String","int","java.lang.String","java.lang.String","android.content.Context","com.renren.mobile.android.loginfree.LoginStatusListener").implementation = function(p1,p2,p3,p4,p5,p6,p7) {
            console.log('=========== m_RSA_login ============');
            console.log('p1 : ' + p1);
            console.log('p2 : ' + p2);
            console.log('p3 : ' + p3);
            console.log('p4 : ' + p4);
            console.log('p5 : ' + p5);
            console.log('=========== m_RSA_login ============');
            var c1 = "17683927317";
            var
            this.m_RSA_login(p1,p2,p3,p4,p5,p6,p7);
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
session = frida.get_usb_device().attach('com.renren.mobile.android')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()