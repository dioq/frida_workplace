# -*- coding: UTF-8 -*-
import frida, sys

jsCode = """
Java.perform(function () {
    /*
    var ShufferMap = Java.use('com.xiaojianbang.app.ShufferMap');
    ShufferMap.show.implementation = function (map) {
        var result = "";
        var keyset = map.keySet();
        var it = keyset.iterator();
        while(it.hasNext()){
            var keystr = it.next().toString();
            var valuestr = map.get(keystr).toString();
            result += valuestr;
        }
        send(result);
        return this.show(map);
    }
    */
    var HashMap = Java.use('java.util.HashMap');
    var ShufferMap = Java.use('com.xiaojianbang.app.ShufferMap');
    ShufferMap.show.implementation = function (map) {
        var hm = HashMap.$new();
        hm.put("user","dajianbang");
        hm.put("pass","87654321");
        hm.put("code","123456");
        return this.show(hm);
    }
});
"""


def message(message, data):
    if message["type"] == 'send':
        print(u"[*] {0}".format(message['payload']))
    else:
        print(message)


process = frida.get_remote_device().attach("com.xiaojianbang.app")

script = process.create_script(jsCode)

script.on("message", message)

script.load()

sys.stdin.read()
