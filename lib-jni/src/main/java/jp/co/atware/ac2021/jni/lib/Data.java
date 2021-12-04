package jp.co.atware.ac2021.jni.lib;

import java.util.List;
import java.util.stream.Stream;
import java.util.stream.IntStream;

import static java.util.stream.Collectors.toList;

public class Data {

    private final List<Integer> values;

    private Data(List<Integer> values) {
        this.values = values;
    }

    public int[] toIntArray() {
        var raw = new int[values.size()];
        IntStream.range(0, values.size()).forEach(i -> raw[i] = values.get(i));
        return raw;
    }

    public static Stream<Data> generateDataStream(int size) {
        return IntStream.range(0, size)
            .map(i -> i % 10 + 1)
            .mapToObj(i -> IntStream.range(0, i).map(v -> i).boxed().collect(toList()))
            .map(Data::new);
    }
}
