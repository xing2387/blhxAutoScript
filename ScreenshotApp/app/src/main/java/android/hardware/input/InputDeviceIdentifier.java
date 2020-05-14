package android.hardware.input;

import android.os.Parcel;
import android.os.Parcelable;


public class InputDeviceIdentifier implements Parcelable {

    public static final Creator<InputDeviceIdentifier> CREATOR = new Creator<InputDeviceIdentifier>() {
        @Override
        public InputDeviceIdentifier createFromParcel(Parcel in) {
            throw new AssertionError("should be a framework class?");
        }

        @Override
        public InputDeviceIdentifier[] newArray(int size) {
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
