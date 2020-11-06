# -*- coding: utf-8 -*-
import frida, sys

jscode = """
if(Java.available){
    Java.perform(function(){   
            var util = Java.use("com.caomeizb1.app.common.utils.SystemUtil");//获取到类
            util.getIMEI.implementation = function() {       
            send("hook Start...")              
            var ret = this.getIMEI();  
            send("原devices=============>"+ret);   
            return "e9794c06d2ce1780f28cc96586f80b01";   
      }                        
            var util = Java.use("io.rong.imlib.model.Message");//获取到类
            util.setTargetId.implementation = function(a) {       
            send("hook Start...")  
            send(a) ;   
            var ret = this.setTargetId("1000000358");                       
    }                  
            var util = Java.use("com.caomeizb1.app.network.user.User");//获取到类
            util.getToken.implementation = function() {       
            send("hook Start...")                  
            var ret = this.getToken();  
            send("原token=============>"+ret);
            return "$2y$10$kNa4W7RlXFMacCcDBTSxXeptrW4nwNKjEYLIjZo207Nn9OXftKqAS.M2CMIMTYwNTIwOTg2OA==";        
      }                 
            var util = Java.use("io.rong.imkit.fragment.ConversationFragment");//获取到类
            util.onSendToggleClick.implementation = function(a,b) {       
            send("hook Start...")  
            send(a) ;   
            send(b);
            var ret = this.onSendToggleClick(a,"约炮搜４ｘｂ．ｃｃ附近肏逼");     
      } 
             
    });
}
"""
def message(message, data):
    if message["type"] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

process = frida.get_remote_device().attach('com.sweet.sugar')
script = process.create_script(jscode)
script.on("message", message)
script.load()
sys.stdin.read()
