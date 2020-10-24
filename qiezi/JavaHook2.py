# -*- coding: utf-8 -*-

import frida
import sys

# HOOK普通方法
jscode = """
Java.perform(function () {
    var secretKeySpec = Java.use('javax.crypto.spec.SecretKeySpec');
    secretKeySpec.$init.overload('[B','java.lang.String').implementation = function (a,b) {
        
        var result = this.$init(a, b);
        send("======================================");
        send("算法名：" + b + "|Dec密钥:" + bytesToString(a));
        send("算法名：" + b + "|Hex密钥:" + bytesToHex(a));
        return result;
    }
    var mac = Java.use('javax.crypto.Mac');
    mac.getInstance.overload('java.lang.String').implementation = function (a) {
        
        var result = this.getInstance(a);
        send("======================================");
        send("算法名：" + a);
        return result;
    }
    mac.update.overload('[B').implementation = function (a) {
       
        this.update(a);
        send("======================================");
        send("update:" + bytesToString(a))
    }
    mac.update.overload('[B','int','int').implementation = function (a,b,c) {
       
        this.update(a,b,c)
        send("======================================");
        send("update:" + bytesToString(a) + "|" + b + "|" + c);
    }
    mac.doFinal.overload().implementation = function () {
       
        var result = this.doFinal();
        send("======================================");
        send("doFinal结果:" + bytesToHex(result));
        send("doFinal结果:" + bytesToBase64(result));
        return result;
    }
    mac.doFinal.overload('[B').implementation = function (a) {
       
        var result = this.doFinal(a);
        send("======================================");
        send("doFinal参数:" + bytesToString(a));
        send("doFinal结果:" + bytesToHex(result));
        send("doFinal结果:" + bytesToBase64(result));
        return result;
    }
        var md = Java.use('java.security.MessageDigest');
    md.getInstance.overload('java.lang.String','java.lang.String').implementation = function (a,b) {
       
        send("======================================");
        send("算法名：" + a);
        return this.getInstance(a, b);
    }
    md.getInstance.overload('java.lang.String').implementation = function (a) {
        
        send("======================================");
        send("算法名：" + a);
        return this.getInstance(a);
    }
    md.update.overload('[B').implementation = function (a) {
        
        send("======================================");
        send("update:" + bytesToString(a))
        return this.update(a);
    }
    md.update.overload('[B','int','int').implementation = function (a,b,c) {
        
        send("======================================");
        send("update:" + bytesToString(a) + "|" + b + "|" + c);
        return this.update(a,b,c);
    }
    md.digest.overload().implementation = function () {
        
        send("======================================");
        var result = this.digest();
        send("digest结果:" + bytesToHex(result));
        send("digest结果:" + bytesToBase64(result));
        return result;
    }
    md.digest.overload('[B').implementation = function (a) {
        
        send("======================================");
        send("digest参数:" + bytesToString(a));
        var result = this.digest(a);
        send("digest结果:" + bytesToHex(result));
        send("digest结果:" + bytesToBase64(result));
        return result;
    }
        var ivParameterSpec = Java.use('javax.crypto.spec.IvParameterSpec');
    ivParameterSpec.$init.overload('[B').implementation = function (a) {
        
        var result = this.$init(a);
        send("======================================");
        send("iv向量:" + bytesToString(a));
        send("iv向量:" + bytesToHex(a));
        return result;
    }
    var cipher = Java.use('javax.crypto.Cipher');
    cipher.getInstance.overload('java.lang.String').implementation = function (a) {
        
        var result = this.getInstance(a);
        send("======================================");
        send("模式填充:" + a);
        return result;
    }
    cipher.update.overload('[B').implementation = function (a) {
        
        var result = this.update(a);
        send("======================================");
        send("update:" + bytesToString(a));
        return result;
    }
    cipher.update.overload('[B','int','int').implementation = function (a,b,c) {
        
        var result = this.update(a,b,c);
        send("======================================");
        send("update:" + bytesToString(a) + "|" + b + "|" + c);
        return result;
    }
    cipher.doFinal.overload().implementation = function () {
       
        var result = this.doFinal();
        send("======================================");
        send("doFinal结果:" + bytesToHex(result));
        send("doFinal结果:" + bytesToBase64(result));
        return result;
    }
    cipher.doFinal.overload('[B').implementation = function (a) {
       
        var result = this.doFinal(a);
        send("======================================");
        send("doFinal参数:" + bytesToString(a));
        send("doFinal结果:" + bytesToHex(result));
        send("doFinal结果:" + bytesToBase64(result));
        return result;
    }
    var x509EncodedKeySpec = Java.use('java.security.spec.X509EncodedKeySpec');
    x509EncodedKeySpec.$init.overload('[B').implementation = function (a) {
        
        var result = this.$init(a);
        send("======================================");
        send("RSA密钥:" + bytesToBase64(a));
        return result;
    }
    var rSAPublicKeySpec = Java.use('java.security.spec.RSAPublicKeySpec');
    rSAPublicKeySpec.$init.overload('java.math.BigInteger','java.math.BigInteger').implementation = function (a,b) {
        showStacks();
        var result = this.$init(a,b);
        send("======================================");
        //send("RSA密钥:" + bytesToBase64(a));
        send("RSA密钥N:" + a.toString(16));
        send("RSA密钥E:" + b.toString(16));
        return result;
    }
        //将byte[]转成String的方法
        
    function bytesToString(arr) {  
        var str = '';
        arr = new Uint8Array(arr);
        for(i in arr){
            str += String.fromCharCode(arr[i]);
        }
        return str;
    }
});
""";

#fw = open(sys.argv[1],'w+',encoding='utf-8')

source = """
    rpc.exports = {
    add: function (a, b) {
        return a + b;
    },
    sub: function (a, b) {
        return new Promise(function (resolve) {
        setTimeout(function () {
            resolve(a - b);
        }, 100);
        });
    }
    };
"""
#
# #HOOK构造方法
# jscode = """
# Java.perform(function () {
#     var money = Java.use('com.qianyu.fridaapp.Money');
#     money.$init.implementation = function (a, b) {
#         console.log("Hook Start...");
#
#         send(arguments[0]);
#         send(arguments[1]);
#
#         return this.$init(10000, arguments[1]);
#     }
# });
# """

#HOOK重载方法
"""jscode =
Java.perform(function () {
   var utils = Java.use('com.qianyu.fridaapp.Utils');
   utils.test.overload("int").implementation = function (a) {
      console.log("Hook Start...");

       send(arguments[0]);

      return "yijinjiaoyu";
   }
});
"""
#
##
# jscode = """
# Java.perform(function () {
#     var utils = Java.use('com.qianyu.fridaapp.Utils');
#     var money = Java.use('com.qianyu.fridaapp.Money');
#     utils.test.overload().implementation = function () {
#         send("Hook Start...");
#         var mon = money.$new(2000,'港币');
#         send(mon.getInfo());
#         return this.test(800);
#     }
# });
# """

#HOOK修改对象属性
# jscode = """
# Java.perform(function () {
#     var utils = Java.use('com.qianyu.fridaapp.Utils');
#     var money = Java.use('com.qianyu.fridaapp.Money');
#     var clazz = Java.use('java.lang.Class');
#     utils.test.overload().implementation = function () {
#         send("Hook Start...");
#         var mon = money.$new(200,"RMB");
#         send(mon.getInfo());
#         var num= Java.cast(mon.getClass(),clazz).getDeclaredField('num');
#         num.setAccessible(true);
#         num.setInt(mon, 2000);
#         send(mon.getInfo());
#         return this.test();
#     }
# });
# """


def message(message, data):
    if message["type"] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

process = frida.get_remote_device().attach('com.qzdsp.tiktok')
script = process.create_script(jscode)
script.on("message", message)
script.load()
sys.stdin.read()

