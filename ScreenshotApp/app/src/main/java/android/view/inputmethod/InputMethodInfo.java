package android.view.inputmethod;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by n7642 on 2018/2/22.
 */

public class InputMethodInfo implements Parcelable {

    public static final Creator<InputMethodInfo> CREATOR = new Creator<InputMethodInfo>() {
        @Override
        public InputMethodInfo createFromParcel(Parcel in) {
            throw new AssertionError("should be a framework class?");
        }

        @Override
        public InputMethodInfo[] newArray(int size) {
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

    public int getNaturalHeight() {
        throw new AssertionError("should be a framework class?");
    }

    public int getNaturalWidth() {
        throw new AssertionError("should be a framework class?");
    }
}
