if (Java.available) {
    Java.perform(function () {
/*        Java.enumerateLoadedClasses({
            onMatch: function (name, handle) {
                if (name.indexOf("com.my.fridademo") != -1) {
                    console.log(name);
                    var clazz = Java.use(name);
                    console.log(clazz);
                    var methods = clazz.class.getDeclaredMethods();
                    for (var i = 0; i < methods.length; i++) {
                        console.log(methods[i]);
                    }
                }
            },
            onComplete: function () {

            }
        });*/

        var classes = Java.enumerateLoadedClassesSync();
        for (var i = 0; i < classes.length; i++) {
            if (classes[i].indexOf("com.my.fridademo") != -1) {
                console.log('=========== get start ============');
                console.log(classes[i]);
                var clazz = Java.use(classes[i]);
                var methods = clazz.class.getDeclaredMethods();
                for (var j = 0; j < methods.length; j++) {
                    console.log(methods[j]);
                }
                console.log('=========== get end ============');
            }
        }
    });
}