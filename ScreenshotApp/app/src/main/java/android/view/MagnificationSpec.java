package android.view;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by n7642 on 2018/2/22.
 */

public class MagnificationSpec implements Parcelable {

    public static final Creator<MagnificationSpec> CREATOR = new Creator<MagnificationSpec>() {
        @Override
        public MagnificationSpec createFromParcel(Parcel in) {
            throw new AssertionError("should be a framework class?");
        }

        @Override
        public MagnificationSpec[] newArray(int size) {
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
