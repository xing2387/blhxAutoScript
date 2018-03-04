package xxx.xxx.screenshotapp;

import android.annotation.SuppressLint;
import android.hardware.display.IDisplayManager;
import android.hardware.input.InputManager;
import android.os.IBinder;
import android.view.IWindowManager;

import java.lang.reflect.Method;

/**
 * Created by n7642 on 2018/2/27.
 */

public class BaseHelper {


    private static Method sServiceManager;
    private static IDisplayManager sDisplayManager;
    private static IWindowManager sWindowsManager;
    private static InputManager sInputManager;

    public BaseHelper() {
    }

    @SuppressLint("PrivateApi")
    public static Method getServiceManager() {
        if (sServiceManager == null) {
            try {
                sServiceManager = Class.forName("android.os.ServiceManager").getDeclaredMethod("getService", String.class);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return sServiceManager;
    }


    @SuppressLint("PrivateApi")
    public static IDisplayManager getDisplayManager() {
        if (sDisplayManager == null) {
            try {
                sDisplayManager = IDisplayManager.Stub.asInterface((IBinder) (getServiceManager()).invoke(null, "display"));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return sDisplayManager;
    }

    @SuppressLint("PrivateApi")
    public static IWindowManager getWindowsManager() {
        if (sWindowsManager == null) {
            try {
                sWindowsManager = IWindowManager.Stub.asInterface((IBinder) (getServiceManager()).invoke(null, "window"));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return sWindowsManager;
    }

    @SuppressLint("PrivateApi")
    public static InputManager getInputManager() {
        if (sInputManager == null) {
            try {
                sInputManager = (InputManager) InputManager.class.getDeclaredMethod("getInstance", new Class[0]).invoke(null);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return sInputManager;
    }
}