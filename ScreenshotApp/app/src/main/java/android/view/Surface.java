/*
 * Copyright (C) 2007 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package android.view;

import android.os.Parcel;
import android.os.Parcelable;

public class Surface implements Parcelable {

    public static final Creator<Surface> CREATOR = new Creator<Surface>() {
        @Override
        public Surface createFromParcel(Parcel in) {
            throw new AssertionError("should be a framework class?");
        }

        @Override
        public Surface[] newArray(int size) {
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

    public Surface() {
        throw new AssertionError("should be a framework class?");
    }

    public void readFromParcel(Parcel source) {
        throw new AssertionError("should be a framework class?");
    }
}
