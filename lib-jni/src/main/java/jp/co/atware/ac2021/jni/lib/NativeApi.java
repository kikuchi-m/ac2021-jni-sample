package jp.co.atware.ac2021.jni.lib;

public class NativeApi {

    public NativeApi() {
        System.loadLibrary("jni-performance-sample");
    }

    public native long calcByArray(long[][] data);

    public native long calcByStream(StreamIterator iter);
}
