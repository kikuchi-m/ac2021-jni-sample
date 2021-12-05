package jp.co.atware.ac2021.jni.app;

import jp.co.atware.ac2021.jni.lib.Data;
import jp.co.atware.ac2021.jni.lib.NativeApi;
import jp.co.atware.ac2021.jni.lib.StreamIterator;

import java.time.Duration;
import java.time.LocalTime;

public class Application {

    public static void main(String... args) {
        System.out.println("JNI performance by stream");
        var nativeApi = new NativeApi();

        // prepare
        var size = Integer.parseInt(args[0]);

        // perform
        var start = LocalTime.now();

        var dataStream = Data.generateDataStream(size);
        var res = nativeApi.calcByStream(StreamIterator.of(dataStream));

        var end = LocalTime.now();

        // result
        var dur = Duration.between(start, end).toMillis() / 1000.0;
        System.out.printf("%sS (start: %s / end: %s)\n", dur, start, end);
        System.out.printf("calculated value: %d\n", res);
    }
}
