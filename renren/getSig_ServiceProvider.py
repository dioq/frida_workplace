# -*- coding: utf-8 -*-

import frida, sys


#HOOK 静态方法 (其实就跟普通方法一样)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.renren.mobile.android.service.ServiceProvider");//获取到类
        util.getSig.implementation = function(strArr, str) {
            var value = this.getSig(strArr,str);
            console.log('=========== getSig  start ============');
            var j = 0;
            for(j = 0; j < strArr.length; j++) {
                console.log(strArr[j]);
            }
            console.log('secretKey : ' + str);
            console.log('sig : ' + value);
            console.log('=========== getSig  end ============');
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
session = frida.get_usb_device().attach('com.renren.mobile.android')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()