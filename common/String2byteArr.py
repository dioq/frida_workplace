# -*- coding: utf-8 -*-
import frida
import sys

# HOOK 二进制数与字符串的转换
jscode = """
Java.perform(function () {
    var login = Java.use('com.qianyu.helloworld.LoginActivity$1');
    var Arrays = Java.use("java.util.Arrays");//获取java.util.Arrays类
    login.onClick.implementation = function (a) {
        send("Hook Start...");
        
        var bytes=stringToBytes("yi jin jiao yu!")
        send(bytes); 
        
        var str=byteToString(bytes)
        send(str);
        
        //打印byte[] 字节数组的二进制
        var bytesStr = Arrays.toString(bytes);
        console.log('bytesStr : ' + bytesStr);
    }
    
    //字符串转byte[]数组
    function stringToBytes(str) {  
        var ch, st, re = []; 
        for(var i = 0; i < str.length; i++ ) { 
            ch = str.charCodeAt(i);  
            st = [];                 
            do{  
                st.push( ch & 0xFF );  
                ch = ch >> 8;          
            }    
            while(ch);  
            re = re.concat(st.reverse()); 
        }  
        return re;  
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
});
"""


def message(message, data):
    if message["type"] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


process = frida.get_remote_device().attach('com.qianyu.helloworld')
script = process.create_script(jscode)
script.on("message", message)
script.load()
sys.stdin.read()
