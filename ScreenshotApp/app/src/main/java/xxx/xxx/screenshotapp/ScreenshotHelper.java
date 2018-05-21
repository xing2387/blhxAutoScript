package xxx.xxx.screenshotapp;

import android.annotation.SuppressLint;
import android.graphics.Bitmap;
import android.graphics.Matrix;
import android.graphics.Point;
import android.os.Build;
import android.os.RemoteException;
import android.view.Display;
import android.view.DisplayInfo;

public class ScreenshotHelper extends BaseHelper {

    private Point mScreenSize;
    private float mScale = 1;       // [0f,1f]
    private int mSize = -1;

    public ScreenshotHelper() {
        mScreenSize = new Point();
    }

    public void getCurrentDisplaySize(Point point) throws Exception {
        DisplayInfo displayInfo = getDisplayManager().getDisplayInfo(Display.DEFAULT_DISPLAY);
        int rotation = getRotation();
        if (rotation == 0 || rotation == 2) {
            point.set(displayInfo.getNaturalWidth(), displayInfo.getNaturalHeight());
        } else {
            point.set(displayInfo.getNaturalHeight(), displayInfo.getNaturalWidth());
        }
    }

    @SuppressLint("PrivateApi")
    public void getDisplayNaturalSize(Point point) throws Exception {

        DisplayInfo displayInfo = getDisplayManager().getDisplayInfo(Display.DEFAULT_DISPLAY);
//        System.out.println("displayInfo, mScreenSize: " +
//                "width=" + displayInfo.getNaturalWidth() + ", height=" + displayInfo.getNaturalHeight());
//        System.out.println("displayInfo: " + displayInfo.toString());
        point.x = displayInfo.getNaturalWidth();
        point.y = displayInfo.getNaturalHeight();
    }

    public int getRotation() {
        try {
            return getWindowsManager().getRotation();
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        return -1;
    }

    public float getScale() {
        return mScale;
    }

    public void setScale(float scale) {
        if (mScale == scale) {
            return;
        }
        this.mSize = -1;
        this.mScale = scale;
    }

    public void setSize(int size) {
        if (size == mSize) {
            return;
        }
        this.mScale = -1;
        this.mSize = size;
    }

    public Point getScreenSize() {
        return mScreenSize;
    }

    @SuppressLint("PrivateApi")
    public Bitmap screenshot() throws Exception {
        getDisplayNaturalSize(mScreenSize);
        String surfaceClassName;
        if (Build.VERSION.SDK_INT <= 17) {
            surfaceClassName = "android.view.Surface";
        } else {
            surfaceClassName = "android.view.SurfaceControl";
        }

        if (mScale < 0) {
            mScale = mSize <= 0 ? 1 : mSize * 1f / Math.min(mScreenSize.x, mScreenSize.y);
        }

        Bitmap b = (Bitmap) Class.forName(surfaceClassName).getDeclaredMethod("screenshot",
                Integer.TYPE, Integer.TYPE).invoke(null, (int) (mScreenSize.x * mScale), (int) (mScreenSize.y * mScale));
        if (b == null) {
            throw new NullPointerException("screenshot method return null !!");
        }

        int rotation = getRotation();
        if (rotation == 0) {
            return b;
        }
        Matrix m = new Matrix();
        if (rotation == 1) {
            m.postRotate(-90.0f);
        } else if (rotation == 2) {
            m.postRotate(-180.0f);
        } else if (rotation == 3) {
            m.postRotate(-270.0f);
        }
        return Bitmap.createBitmap(b, 0, 0, mScreenSize.x, mScreenSize.y, m, false);
    }

}
