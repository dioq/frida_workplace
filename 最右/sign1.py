# -*- coding: utf-8 -*-

import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.izuiyou.network.NetCrypto");//获取到类
        var Arrays = Java.use("java.util.Arrays");
        util.f.overload("java.lang.String","[B").implementation = function(param,p2) {
            var result = this.f(param,p2);
            console.log('=========== f start ============');
            console.log('param : ' + param);
            console.log('p2 : ' + p2);
            var p2Str = Arrays.toString(p2);
            console.log('p2Str : ' + p2Str);
            //var p2Str = byteToString(p2);
            //console.log('p2Str : ' + p2Str);
            console.log('result : ' + result);
            console.log('=========== f end   ============');
            return result;
        }
        
       function byteToString(arr){  
            if(typeof arr === 'string'){  
                return arr;  
            }  
            var str='',  
            _arr = arr;  
            for(var i=0; i<_arr.length; i++) {  
                var one =_arr[i].toString(2), v=one.match(/^1+?(?=0)/);  
                if(v && one.length == 8){  
                    var bytesLength = v[0].length;  
                    var store = _arr[i].toString(2).slice(7 - bytesLength);  
                    for(var st=1; st < bytesLength; st++) {  
                        store+=_arr[st + i].toString(2).slice(2);  
                    }  
                    str+=String.fromCharCode(parseInt(store, 2));  
                    i+=bytesLength-1;  
                } else {  
                    str+=String.fromCharCode(_arr[i]);  
                }  
            }  
            return str;  
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
