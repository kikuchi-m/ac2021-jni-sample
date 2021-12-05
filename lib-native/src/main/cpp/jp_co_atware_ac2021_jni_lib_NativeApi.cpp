#include "jp_co_atware_ac2021_jni_lib_NativeApi.h"

#include <jni.h>

jlong Java_jp_co_atware_ac2021_jni_lib_NativeApi_calcByArray(JNIEnv* env, jobject, jobjectArray data) {

    jlong result = 0;
    auto dataSize = env->GetArrayLength(data);

    for (jsize i = 0; i < dataSize; ++i) {
        auto d = (jlongArray) env->GetObjectArrayElement(data, i);
        auto ds = env->GetArrayLength(d);
        auto dPtr = env->GetLongArrayElements(d, JNI_FALSE);
        for (jsize di = 0; di < ds; ++di) {
            result += dPtr[di];
        }
        env->ReleaseLongArrayElements(d, dPtr, JNI_ABORT);
    }
    return result;
}

jlong Java_jp_co_atware_ac2021_jni_lib_NativeApi_calcByStream(JNIEnv* env, jobject, jobject iter) {
    auto streamIterator = env->FindClass("jp/co/atware/ac2021/jni/lib/StreamIterator");
    auto hasNext = env->GetMethodID(streamIterator, "hasNext", "()Z");
    auto next = env->GetMethodID(streamIterator, "next", "()[J");
    jlong result = 0;

    while (env->CallBooleanMethod(iter, hasNext)) {
        auto d = (jlongArray) env->CallObjectMethod(iter, next);
        auto ds = env->GetArrayLength(d);
        auto dPtr = env->GetLongArrayElements(d, JNI_FALSE);
        for (jsize di = 0; di < ds; ++di) {
            result += dPtr[di];
        }
        env->ReleaseLongArrayElements(d, dPtr, JNI_ABORT);
    }
    return result;
}

jlong Java_jp_co_atware_ac2021_jni_lib_NativeApi_calcByStreamChunk(JNIEnv* env, jobject, jobject iter) {
    auto streamIterator = env->FindClass("jp/co/atware/ac2021/jni/lib/StreamIterator");
    auto hasNext = env->GetMethodID(streamIterator, "hasNext", "()Z");
    auto nextChunk = env->GetMethodID(streamIterator, "nextChunk", "()[[J");
    jlong result = 0;

    while (env->CallBooleanMethod(iter, hasNext)) {
        auto dc = (jobjectArray) env->CallObjectMethod(iter, nextChunk);
        auto dcs = env->GetArrayLength(dc);
        for (jsize dci = 0; dci < dcs; ++dci) {
            auto d = (jlongArray) env->GetObjectArrayElement(dc, dci);
            auto ds = env->GetArrayLength(d);
            auto dPtr = env->GetLongArrayElements(d, JNI_FALSE);
            for (jsize di = 0; di < ds; ++di) {
                result += dPtr[di];
            }
            env->ReleaseLongArrayElements(d, dPtr, JNI_ABORT);
        }
    }
    return result;
}
