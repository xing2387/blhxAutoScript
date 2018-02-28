package android.view;

import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by n7642 on 2018/2/22.
 */

public class AppTransitionAnimationSpec implements Parcelable {

    public static final Creator<AppTransitionAnimationSpec> CREATOR = new Creator<AppTransitionAnimationSpec>() {
        @Override
        public AppTransitionAnimationSpec createFromParcel(Parcel in) {
            throw new AssertionError("should be a framework class?");
        }

        @Override
        public AppTransitionAnimationSpec[] newArray(int size) {
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
