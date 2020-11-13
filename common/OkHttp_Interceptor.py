# -*- coding: utf-8 -*-
import frida, sys

# HOOK OkHttp的请求Interceptor
jscode = """
if (Java.available) {
    Java.perform(function () {
        var Interceptor = Java.use("okhttp3.Interceptor");
        var Gson = Java.use("com.google.gson.Gson");
        var MyInterceptor = Java.registerClass({
            name: "okhttp3.MyInterceptor",
            implements: [Interceptor],
            methods: {
                intercept: function (chain) {
                    //网络请求 request
                    var request = chain.request();
                    var gson = Gson.$new();
                    var request_json = gson.toJson(request);
                    console.log("request json : " + request_json);

                    //返回值
                    var response = chain.proceed(request);
                    try {
                        var responseBody = response.body();
                        var contentLength = responseBody ? responseBody.contentLength() : 0;
                        if (contentLength > 0) {
                            var ContentType = response.headers().get("Content-Type");
                            if (ContentType.indexOf("video") == -1) {
                                if (ContentType.indexOf("application") == 0) {
                                    var source = responseBody.source();
                                    if (ContentType.indexOf("application/zip") != 0) {
                                        try {
                                            console.log("response.body StringClass :", source.readUtf8());
                                        } catch (error) {
                                            try {
                                                console.log("response.body ByteString", source.readByteString().hex());
                                            } catch (error) {
                                                console.log("error 4:", error);
                                            }
                                        }
                                    }
                                }

                            }

                        }

                    } catch (error) {
                        console.log("error 3:", error);
                    }
                    return response;
                }
            }
        });

        var ArrayList = Java.use("java.util.ArrayList");
        var OkHttpClient = Java.use("okhttp3.OkHttpClient");
        OkHttpClient.$init.overload('okhttp3.OkHttpClient$Builder').implementation = function (Builder) {
            //console.log("OkHttpClient.$init:", this, Java.cast(Builder.interceptors(), ArrayList));
            this.$init(Builder);
        };

        var MyInterceptorObj = MyInterceptor.$new();
        var Builder = Java.use("okhttp3.OkHttpClient$Builder");
        Builder.build.implementation = function () {
            this.interceptors().clear();
            this.interceptors().add(MyInterceptorObj);
            var result = this.build();
            return result;
        };

        Builder.addInterceptor.implementation = function (interceptor) {
            this.interceptors().clear();
            this.interceptors().add(MyInterceptorObj);
            return this;
        };
    });
}
"""


def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)


# 查找USB设备并附加到目标进程
session = frida.get_usb_device().attach('com.my.network')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
