
let carrierName = "TAC";//泰国的三大电信运营商：True Corp, AIS, TAC
let IDFA = "E621E1F8-8888-495A-93FC-0C247A3E6E5F"; // 广告标识
let IDFV = "E621E1F8-8888-495A-93FC-0C247A3E6E5F"; // 也就是 uuid 序列号 唯一标识符
let iPhoneName = "newPhone"; // 手机名字
let localizedModel = "iPhone";//设备区域化型号
let systemName = "iPad OS";// 系统名称
let systemVersion = "12.4.1";// 系统版本

// 系统内核相关
let sysname="Darwin\0";
let nodename="newName\0"; // 手机名字
let release="21.5.0\0";
let version="Darwin Kernel Version 21.5.0: Thu Apr 21 21:51:23 PDT 2022; root:xnu-8020.122.1~1/RELEASE_ARM64_T8010\0";
let machine="iPhone8,4\0";

// app 信息
let bundleID = "com.tencent.xin";

if (ObjC.available) { //判断Object-C类方法是否已经加载进来
    setImmediate(hook_carrierName);
    setImmediate(hood_IDFA);
    setImmediate(hood_IDFV);
    setImmediate(hook_iPhoneName);
    setImmediate(hook_localizedModel);
    setImmediate(hook_systemName);
    setImmediate(hook_systemVersion);
    setImmediate(utsname_hook);
    // setImmediate(infoDictionary_hook);
    // setTimeout(infoDictionary_hook, 15);
    // setImmediate(bundleIdentifier_hook);
}

//字符串转byte[]数组
function stringToBytes(str) {
    var ch, st, re = [];
    for (var i = 0; i < str.length; i++) {
        ch = str.charCodeAt(i);
        st = [];
        do {
            st.push(ch & 0xFF);
            ch = ch >> 8;
        }
        while (ch);
        re = re.concat(st.reverse());
    }
    return re;
}

// hook 通过 info.plist 获取 app 信息的方法
function infoDictionary_hook() {
    console.log("hook infoDictionary is running ...")
    let class_name = 'NSBundle'
    var method_name = "- infoDictionary";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的info.plist :", ret2);
        var NSMutableDictionary = ObjC.classes.NSMutableDictionary;
        var mutableDict = NSMutableDictionary.dictionaryWithDictionary_(ret2);
        // 修改内容
        mutableDict['- setValue:forKey:'](bundleID,'CFBundleIdentifier');
        console.log("新的info.plist :", mutableDict);

        return mutableDict;
    })
}

// 这里 hook 的不是最底层, 上面 infoDictionary 里获取的 app 信息才是最底层
function bundleIdentifier_hook() {
    console.log("hook bundleIdentifier is running ...")
    let class_name = 'NSBundle'
    var method_name = "- bundleIdentifier";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的bundleIdentifier :", ret2)
        let ret_change = ObjC.classes.NSString.stringWithString_(bundleID);
        return ret_change
    })
}


function utsname_hook() {
    console.log("hook utsname is running ...")
    let func_name = "uname";
    // 函数所在动态库设为null,则在整个可执行文件里面寻找 symbol
    var n_addr_func = Module.findExportByName(null, func_name);

    // 在目标进程里开辟内存,并填入二进制数据.我这里是构造一个 struct 作为函数新的参数.
    var size = 256 * 5;
    var my_struct = Memory.alloc(size);
    // st.writeByteArray([0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41]);
    // let data = utsname;
    let sysname_arr = stringToBytes(sysname);
    let nodename_arr = stringToBytes(nodename);
    let release_arr = stringToBytes(release);
    let version_arr = stringToBytes(version);
    let machine_arr = stringToBytes(machine);
    // var struct_binary = new Array();

    var param_struct = null; // 全局变量

    try {
        Interceptor.attach(n_addr_func, {
            onEnter: function (args) {
                console.log("onEnter ...");
                param_struct = args[0];// 将原来的 struct 指针取出来,便于在函数调用结束时进行修改
                // args[0] = my_struct;

                // console.log("arg1:", Memory.readCString(args[1]));
            },
            onLeave: function (retval) {
                console.log("onLeave ...");
                // console.log("my_struct:", my_struct);
                // console.log("my_struct value:", Memory.readCString(my_struct));
                param_struct.writeByteArray(sysname_arr);
                param_struct.add(256 * 1).writeByteArray(nodename_arr);
                param_struct.add(256 * 2).writeByteArray(release_arr);
                param_struct.add(256 * 3).writeByteArray(version_arr);
                param_struct.add(256 * 4).writeByteArray(machine_arr);
            },
        })

    } catch (err) {
        console.log("err:" + err + ", trace" + err.stack);
    }
}

function hook_systemVersion() {
    console.log("hook ssystemVersion is running ...")
    let class_name = 'UIDevice'
    var method_name = "- systemVersion";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的systemVersion :", ret2)
        let ret_change = ObjC.classes.NSString.stringWithString_(systemVersion);
        console.log("新的systemVersion :", ret_change)
        return ret_change
    })
}

function hook_systemName() {
    console.log("hook systemName is running ...")
    let class_name = 'UIDevice'
    var method_name = "- systemName";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的systemName :", ret2)
        let ret_change = ObjC.classes.NSString.stringWithString_(systemName);
        return ret_change
    })
}

// hook 运营商
function hook_carrierName() {
    console.log("hook carrierName is running ...")
    let class_name = 'CTCarrier'
    var method_name = "- carrierName";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的运营商 :", ret2)
        let ret_change = ObjC.classes.NSString.stringWithString_(carrierName);
        return ret_change
    })
}

function hood_IDFA() {
    console.log("hook IDFA is running ...");
    let class_name = 'ASIdentifierManager';
    var method_name = "- advertisingIdentifier";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的IDFA :", ret2)
        let ret_change = ObjC.classes.NSString.stringWithString_(IDFA);
        let obj = ObjC.classes.NSUUID['new']()
        let ret = obj['- initWithUUIDString:'](ret_change)
        return ret;
    })
}

function hood_IDFV() {
    console.log("hook IDFV is running ...")
    let class_name = 'UIDevice'
    var method_name = "- identifierForVendor";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的IDFV :", ret2)
        let ret_change = ObjC.classes.NSString.stringWithString_(IDFV);
        let obj = ObjC.classes.NSUUID['new']()
        let ret = obj['- initWithUUIDString:'](ret_change)
        return ret;
    })
}

function hook_iPhoneName() {
    console.log("hook iPhone Name is running ...");
    let class_name = 'UIDevice'
    var method_name = "- name";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的iPhone Name :", ret2)
        let ret_change = ObjC.classes.NSString.stringWithString_(iPhoneName);
        return ret_change
    })
}

function hook_localizedModel() {
    console.log("hook localizedModel is running ...")
    let class_name = 'UIDevice'
    var method_name = "- localizedModel";
    let sharedInstance = ObjC.classes[class_name][method_name]
    let oldImpl = sharedInstance.implementation
    sharedInstance.implementation = ObjC.implement(sharedInstance, function (handle, selector) {
        let ret1 = oldImpl(handle, selector)
        let ret2 = new ObjC.Object(ret1)
        console.log("原来的localizedModel :", ret2)
        let ret_change = ObjC.classes.NSString.stringWithString_(localizedModel);
        return ret_change;
    })
}
