# -*- coding: utf-8 -*-
import frida, sys

# HOOK java.security.MessageDigest 中的加密方法 digest, 这个方法是MD5加密的返回值
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("java.security.MessageDigest");//获取到类
        var Arrays = Java.use("java.util.Arrays");//获取java.util.Arrays类

        util.update.overload("[B").implementation = function(param) {
            this.update(param);
            console.log('=========== 加密参数 update start ============');
            var paramStr1 = Bytes2HexString(param);
            var paramStr2 = byteToString(param);
            console.log('paramStr hex : \\n' + paramStr1);
            console.log('paramStr org : \\n' + paramStr2);
        }


        util.digest.overload().implementation = function() {
            var result = this.digest();
            console.log('=========== 加密结果 digest start ============');
            //打印byte[] 数组的二进制
            var bytesStr = Bytes2HexString(result);
            console.log('result bytesStr : \\n' + bytesStr);
            return result;
        }

        //byte[]数组转字符串
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

        //字节数组转十六进制字符串，对负值填坑
        function Bytes2HexString(arrBytes) {
            var str = "";
            for (var i = 0; i < arrBytes.length; i++) {
                var tmp;
                var num = arrBytes[i];
                if (num < 0) {
                    //此处填坑，当byte因为符合位导致数值为负时候，需要对数据进行处理
                    tmp = (255 + num + 1).toString(16);
                } else {
                    tmp = num.toString(16);
                }
                if (tmp.length == 1) {
                    tmp = "0" + tmp;
                }
                str += tmp;
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
session = frida.get_usb_device().attach('com.lalamove.huolala.client')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
