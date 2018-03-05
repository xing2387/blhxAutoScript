package android.view;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by n7642 on 2018/2/22.
 */

public interface WindowManager extends ViewManager {

    public static class LayoutParams implements Parcelable {

        public static final Creator<LayoutParams> CREATOR = new Creator<LayoutParams>() {
            @Override
            public LayoutParams createFromParcel(Parcel in) {
                throw new AssertionError("should be a framework class?");
            }

            @Override
            public LayoutParams[] newArray(int size) {
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

    public Display getDefaultDisplay();
}
