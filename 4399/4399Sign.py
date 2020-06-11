# -*- coding: utf-8 -*-

import frida, sys


#HOOK 静态方法 (其实就跟普通方法一样)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.m4399.framework.providers.SignDataProvider");//获取到类
        util.buildSignValue.implementation = function(param) {
            var value = this.buildSignValue(param);
            console.log('=========== buildSignValue  start ============');
            console.log('param : ' + param);
            console.log('value : ' + value);
            console.log('=========== buildSignValue  end ============');
            return value;
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
session = frida.get_usb_device().attach('com.m4399.gamecenter')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()