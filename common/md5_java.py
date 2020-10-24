# -*- coding: utf-8 -*-
import frida, sys

#HOOK java.security.MessageDigest 中的加密方法 digest, 这个方法是MD5加密的返回值
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("java.security.MessageDigest");//获取到类
        var Arrays = Java.use("java.util.Arrays");//获取java.util.Arrays类
        
        util.update.overload("[B").implementation = function(param) {
            this.update(param);
            console.log('=========== update start ============');
            console.log('param : ' + param);
            var paramStr = byteToString(param);
            console.log('paramStr : ' + paramStr);
            console.log('=========== update end   ============');
        }
        
        
        util.digest.overload().implementation = function() {
            var result = this.digest();
            console.log('=========== digest start ============');
            console.log('result : ' + result);
            //打印byte[] 数组的二进制
            var bytesStr = Arrays.toString(result);
            console.log('bytesStr : ' + bytesStr);
            console.log('=========== digest end   ============');
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
