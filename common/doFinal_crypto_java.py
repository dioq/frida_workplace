# -*- coding: utf-8 -*-
import frida, sys

# HOOK javax.crypto.Cipher 中的通用加密方法 doFinal
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("javax.crypto.Cipher");//获取到类
        util.doFinal.overload("[B").implementation = function(param) {
            //console.log('=========== doFinal start ============');
            //console.log('param : ' + param);
            var param_hex_str = Bytes2HexString(param);

            var result = this.doFinal(param);
            //console.log('result : ' + result);
            //打印byte[] 数组 转16进制 字符串
            var result_hex_str = Bytes2HexString(result);
            console.log('param_hex_str : \\n' + param_hex_str,'\\nresult_hex_str : \\n' + result_hex_str);
            //console.log('=========== doFinal end   ============');
            return result;
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
session = frida.get_usb_device().attach('com.wuba')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
