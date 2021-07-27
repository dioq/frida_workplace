/*
* java层的SSL 明文加解密的地方hook不住,只能在native里hook SO层里的 SSL 加解密明文的地方,打印出来
* */

// 将所有函数名和对应的偏移保存到  addresses 字典里
var addresses = {};

setImmediate(function () {

    var resolver = new ApiResolver("module");
    var exps = [
        "*libssl*", ["SSL_read", "SSL_write"]
    ];
    var lib = exps[0];
    var names = exps[1];
    for (var j = 0; j < names.length; j++) {
        var name = names[j];
        console.log("exports:" + lib + "!" + name);
        var matches = resolver.enumerateMatchesSync("exports:" + lib + "!" + name);
        // console.log("matches : \n" + matches);
        console.log("name : " + name);
        console.log("matches[0].address : " + matches[0].address);
        addresses[name] = matches[0].address;
    }

});


Interceptor.attach(addresses["SSL_read"],
    {
        onEnter: function (args) {
            // console.log("SSL_read  args[1] : " + args[1]);
            this.buf = args[1];
        },
        onLeave: function (retval) {
            retval |= 0; // Cast retval to 32-bit integer.
            if (retval <= 0) {
                return;
            }
            // console.log("SSL_read retval : " + retval);
            console.log(Memory.readByteArray(this.buf, retval));
        }
    });

Interceptor.attach(addresses["SSL_write"],
    {
        onEnter: function (args) {
            // console.log("SSL_write args[2] : " + args[2]);
            console.log(Memory.readByteArray(args[1], parseInt(args[2])));
        },
        onLeave: function (retval) {
        }
    });
