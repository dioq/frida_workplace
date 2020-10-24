# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.fanwe.live.appview.room.RoomInfoView");//获取到类
        util.clickFollow.implementation = function(){
            console.log("Hook Start...");
            this.clickFollow();
            console.log("Hook Start 2...");
            //var num = 0;
            //setInterval(function () {
            //    console.log("num = " + num);
            //   num++;
            //    this.clickFollow();
            //}, 5 * 1000);
        }
        
        //参数n为休眠时间，单位为毫秒:
        function sleep(n) {
            var start = new Date().getTime();
            console.log('休眠前：' + start);
            while (true) {
                if (new Date().getTime() - start > n) {
                    break;
                }
            }
            console.log('休眠后：' + new Date().getTime());
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
session = frida.get_usb_device().attach('com.liveapp.live')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
