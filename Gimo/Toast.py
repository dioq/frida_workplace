# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("android.widget.Toast");//获取到类
        util.makeText.overload("android.content.Context","java.lang.CharSequence","int").implementation = function(p1,p2,p3){
            var ret = this.makeText(p1,p2,p3);
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
