package android.hardware.input;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by n7642 on 2018/2/22.
 */

public class TouchCalibration implements Parcelable {

    public static final Creator<TouchCalibration> CREATOR = new Creator<TouchCalibration>() {
        @Override
        public TouchCalibration createFromParcel(Parcel in) {
            throw new AssertionError("should be a framework class?");
        }

        @Override
        public TouchCalibration[] newArray(int size) {
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
