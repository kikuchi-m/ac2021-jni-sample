package jp.co.atware.ac2021.jni.app;

import jp.co.atware.ac2021.jni.lib.Data;
import jp.co.atware.ac2021.jni.lib.NativeApi;

import java.time.Duration;
import java.time.LocalTime;
import java.util.List;
import java.util.stream.IntStream;

import static java.util.stream.Collectors.toList;

public class Application {

    public static void main(String... args) {
        System.out.println("JNI performance by array");
        var nativeApi = new NativeApi();

        // prepare
        var size = Integer.parseInt(args[0]);

        // perform
        var start = LocalTime.now();

        var dataStream = Data.generateDataStream(size);
        var data = new int[size][];
        var dataList = dataStream.collect(toList());
        for (var i = 0; i < size; i++) {
            data[i] = dataList.get(i).toIntArray();
        }
        var res = nativeApi.calcByArray(data);

        var end = LocalTime.now();

        // result
        var dur = Duration.between(start, end);
        System.out.printf("%s (start: %s / end: %s)\n", dur, start, end);
        System.out.printf("calculated value: %d\n", res);
    }
}
