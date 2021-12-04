package jp.co.atware.ac2021.jni.app;

import jp.co.atware.ac2021.jni.lib.NativeApi;

public class Application {

    public static void main(String... args) {
        System.out.println("JNI performance by stream");
        new NativeApi();
    }
}
