# -*- coding: utf-8 -*-

import frida, sys

#HOOK 静态方法 (其实就跟普通方法一样)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.renren.mobile.utils.json.JsonObject");//获取到类
        util.getKeys.implementation = function() {
            var value = this.getKeys();
            console.log('=========== start ============');
           //if(value instanceof Array){
                //for(str in value){
                  //  console.log(str);
               // }
                
                var j = 0;
                for(j = 0; j < value.length; j++) {
                   console.log(value[j]);
                }
            //}
            console.log('=========== end ============');
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