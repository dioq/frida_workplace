# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.lalamove.huolala.module.common.utils.ParamsUtil");//获取到类
        util.getSignParamsStr.overload("java.util.Map").implementation = function(map){
            console.log("Hook Start...");
            console.log("p1 : " + map);
            var result = "";
            var keyset = map.keySet();
            var it = keyset.iterator();
            while(it.hasNext()){
                var keystr = it.next().toString();
                var valuestr = map.get(keystr).toString();
                result += valuestr + "  ";
            }
            send(result);
            var ret = this.getSignParamsStr(map);
            console.log("ret : " + ret);
            return ret;
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
