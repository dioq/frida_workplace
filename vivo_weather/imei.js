//Url 的初始化方法
if (Java.available) {
    Java.perform(function () {
        var util = Java.use("com.vivo.vcodecommon.ImeiUtils");//获取到类
        util.getImei.implementation = function (param1) {
            console.log(param1);
            var ret = this.getImei(param1);
            return ret;
        }
    });
}