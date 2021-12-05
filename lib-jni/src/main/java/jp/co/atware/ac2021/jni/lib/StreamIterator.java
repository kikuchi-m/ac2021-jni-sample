package jp.co.atware.ac2021.jni.lib;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.stream.Stream;

public class StreamIterator {

    private final Iterator<Data> iter;
    private final int chunkSize;

    private StreamIterator(Stream<Data> dataStream, int chunkSize) {
        this.iter = dataStream.iterator();
        this.chunkSize = chunkSize;
    }

    public static StreamIterator of(Stream<Data> dataStream) {
        return new StreamIterator(dataStream, 10);
    }

    public static StreamIterator of(Stream<Data> dataStream, int chunkSize) {
        return new StreamIterator(dataStream, chunkSize);
    }

    public boolean hasNext() {
        return iter.hasNext();
    }

    public long[] next() {
        return iter.next().toPrimitiveArray();
    }

    public long[][] nextChunk() {
        var chunk = new ArrayList<long[]>(chunkSize);
        while (iter.hasNext() && chunk.size() < chunkSize) {
            chunk.add(iter.next().toPrimitiveArray());
        }
        return chunk.stream().toArray(long[][]::new);
    }
}
