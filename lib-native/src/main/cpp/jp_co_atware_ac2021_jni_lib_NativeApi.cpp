#include "jp_co_atware_ac2021_jni_lib_NativeApi.h"

#include <jni.h>

jlong Java_jp_co_atware_ac2021_jni_lib_NativeApi_calcByArray(JNIEnv* env, jobject, jobjectArray data) {

    jlong result = 0;
    auto dataSize = env->GetArrayLength(data);

    for (jsize i = 0; i < dataSize; ++i) {
        auto d = (jintArray) env->GetObjectArrayElement(data, i);
        auto ds = env->GetArrayLength(d);
        auto dPtr = env->GetIntArrayElements(d, JNI_FALSE);
        for (jsize di = 0; di < ds; ++di) {
            result += dPtr[di];
        }
        env->ReleaseIntArrayElements(d, dPtr, JNI_ABORT);
    }
    return result;
}

jlong Java_jp_co_atware_ac2021_jni_lib_NativeApi_calcByStream(JNIEnv* env, jobject, jobject iter) {
    return 0;
}
