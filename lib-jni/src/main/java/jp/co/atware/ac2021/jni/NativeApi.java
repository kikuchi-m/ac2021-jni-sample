package jp.co.atware.ac2021.jni;

public class NativeApi {

    public NativeApi() {
        System.loadLibrary("jni-performance-sample");
    }

    native long calcByArray(int[][] data);

    native long calcByStream(StreamIterator iter);
}
