# -*- coding: utf-8 -*-
import frida, sys

#HOOK Url初始化方法
jscode = """
if(Java.available){
    Java.perform(function(){
        Java.choose("com.tianmao.phone.views.LiveRoomViewHolder",{
            onMatch:function(instance){
                console.log("hook start ...");
                var p1 = 1;
                var p2 = "26";
                var p3 = 177710;
                var p4 = "{\"content\":\"<font color=\"#72f3e1\">手机用户1749</font><font color=\"#ffffff\">在</font><font color=\"#fff292\">一分快三</font><font color=\"#ffffff\">投注玩法</font><font color=\"#fff292\">总和_小</font><font color=\"#ffffff\">赢得</font><font color=\"#f9d347\">392</font><font color=\"#ffffff\">元。</font>\"}";
                instance.setShowBarrage(p1,p2,p3,p4);
            },onComplete:function(){}
        })
    });
}
"""

def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)

# 查找USB设备并附加到目标进程
session = frida.get_usb_device().attach('com.tmfeiji11.phonelive1237')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()