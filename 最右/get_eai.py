# -*- coding: utf-8 -*-

import frida, sys

#HOOK navtive方法(就跟hook普通方法是一样的)
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("eai");//获取到类
        util.get.overload("java.lang.String").implementation = function(p1){
            var result = this.get(p1);
            console.log('=========== get start ============');
            console.log('p1 : ' + p1);
            console.log('this.fdU : ' + this.fdU);
            console.log('this.fdU.length : ' + this.fdU.length);
            var j = 0;
            for (j = 0; j < this.fdU.length; j++) {
                console.log(this.fdU[j]);
            }
            console.log('result : ' + result);
            console.log('=========== get end   ============');
            return result;
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
session = frida.get_usb_device().attach('cn.xiaochuankeji.tieba')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()