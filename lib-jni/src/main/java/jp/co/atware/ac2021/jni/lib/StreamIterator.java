package jp.co.atware.ac2021.jni.lib;

import java.util.Iterator;
import java.util.stream.Stream;

public class StreamIterator {

    private final Iterator<Data> iter;

    private StreamIterator(Stream<Data> dataStream) {
        this.iter = dataStream.iterator();
    }

    public static StreamIterator of(Stream<Data> dataStream) {
        return new StreamIterator(dataStream);
    }

    public boolean hasNext() {
        return iter.hasNext();
    }

    public long[] next() {
        return iter.next().toPrimitiveArray();
    }
}
