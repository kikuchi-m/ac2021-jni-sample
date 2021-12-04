package jp.co.atware.ac2021.jni.lib;

import java.util.List;
import java.util.stream.Stream;
import java.util.stream.IntStream;

import static java.util.stream.Collectors.toList;

public class Data {

    private final List<Long> values;

    private Data(List<Long> values) {
        this.values = values;
    }

    public long[] toPrimitiveArray() {
        var raw = new long[values.size()];
        IntStream.range(0, values.size()).forEach(i -> raw[i] = values.get(i));
        return raw;
    }

    public static Stream<Data> generateDataStream(int size) {
        return IntStream.range(0, size)
            .map(i -> i % 10 + 1)
            .mapToObj(i -> IntStream.range(0, i).mapToLong(v -> i).boxed().collect(toList()))
            .map(Data::new);
    }
}
