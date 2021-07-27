# -*- coding: utf-8 -*-
import frida, sys

# HOOK 打印所有的类及方法
jscode = """
if(Java.available){
    Java.perform(function(){
    /*    Java.enumerateLoadedClasses({
            onMatch: function (name, handle) {
                if (name.indexOf("com.yhxk.qpgame.pipi") != -1) {
                    console.log(name);
                    var clazz = Java.use(name);
                    console.log(clazz);
                    var methods = clazz.class.getDeclaredMethods();
                    for (var i = 0; i < methods.length; i++) {
                        console.log(methods[i]);
                    }
                }
            },
            onComplete: function () {

            }
        });
    */
    
        var classes = Java.enumerateLoadedClassesSync();
        for (var i = 0; i < classes.length; i++) {
            // if(classes[i].indexOf("com.yhxk.qpgame.pipi") != -1){
            console.log('=========== get start ============');
            console.log(classes[i]);
            var clazz = Java.use(classes[i]);
            var methods = clazz.class.getDeclaredMethods();
            for (var j = 0; j < methods.length; j++) {
                console.log(methods[j]);
                //   }
                console.log('=========== get end ============');
            }
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
session = frida.get_usb_device().attach('com.yhxk.qpgame.pipi')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
