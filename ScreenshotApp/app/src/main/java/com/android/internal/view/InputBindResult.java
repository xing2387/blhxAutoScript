package com.android.internal.view;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by n7642 on 2018/2/22.
 */

public class InputBindResult implements Parcelable {

    public static final Creator<InputBindResult> CREATOR = new Creator<InputBindResult>() {
        @Override
        public InputBindResult createFromParcel(Parcel in) {
            throw new AssertionError("should be a framework class?");
        }

        @Override
        public InputBindResult[] newArray(int size) {
            throw new AssertionError("should be a framework class?");
        }
    };

    @Override
    public int describeContents() {
        throw new AssertionError("should be a framework class?");
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        throw new AssertionError("should be a framework class?");
    }
}
