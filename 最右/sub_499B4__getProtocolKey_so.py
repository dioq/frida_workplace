# -*- coding: utf-8 -*-

import frida, sys
#HOOK so 文件
jscode = """
setImmediate(function () {
    //通过模块名直接查找基址
    var baseSOFile = Module.findBaseAddress("libnet_crypto.so");
    Interceptor.attach(baseSOFile.add(0x000499B5),{
        onEnter: function(args) {
            console.log('=========== sub_499B4 args start ============');
            console.log(args[0]);
            console.log('=========== sub_499B4 args end   ============');
        },
        onLeave: function(retval){
            console.log('=========== sub_499B4 retval start ============');
            console.log("返回值:"+retval);
            console.log('=========== sub_499B4 retval end   ============');
        }
    });
});
"""

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

process = frida.get_usb_device().attach('com.my.zhuiyou_Crack')
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()
