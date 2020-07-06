package xxx.xxx.screenshotapp;

import android.annotation.SuppressLint;
import android.graphics.Path;
import android.graphics.PathMeasure;
import android.graphics.Point;
import android.graphics.PointF;
import android.hardware.input.InputManager;
import android.os.Looper;
import android.os.RemoteException;
import android.os.SystemClock;
import android.util.Log;
import android.view.InputDevice;
import android.view.InputEvent;
import android.view.KeyCharacterMap;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.RelativeLayout;

import com.android.internal.view.IInputMethodManager;
import com.koushikdutta.async.http.WebSocket;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/**
 * Created by n7642 on 2018/2/27.
 */

public class InputHelper extends BaseHelper {

    private static final String TAG = "screenshotapp";

    private static WebSocket.StringCallback sInputEventCallback;

    private final static HashMap<String, Integer> sKeyCodeMap = new HashMap<String, Integer>() {{
        put("home", KeyEvent.KEYCODE_HOME);
        put("delete", KeyEvent.KEYCODE_FORWARD_DEL);
        put("backspace", KeyEvent.KEYCODE_DEL);
        put("up", KeyEvent.KEYCODE_DPAD_UP);
        put("down", KeyEvent.KEYCODE_DPAD_DOWN);
        put("left", KeyEvent.KEYCODE_DPAD_LEFT);
        put("right", KeyEvent.KEYCODE_DPAD_RIGHT);
        put("back", KeyEvent.KEYCODE_BACK);
        put("menu", KeyEvent.KEYCODE_MENU);
        put("recent", KeyEvent.KEYCODE_APP_SWITCH);
    }};

    private static KeyCharacterMap mKeyCharacterMap;


    private static void injectMotionEvent(InputManager inputManager, Method injectInputEventMethod,
                                          int source, int action, long downTime, long eventTime,
                                          float x, float y, float yPrecision) {
        MotionEvent.PointerProperties[] pointerProperties = new MotionEvent.PointerProperties[1];
        pointerProperties[0] = new MotionEvent.PointerProperties();
        pointerProperties[0].clear();
        pointerProperties[0].toolType = MotionEvent.TOOL_TYPE_FINGER;
        pointerProperties[0].id = 0;
        MotionEvent.PointerCoords[] pointerCoords = new MotionEvent.PointerCoords[1];
        pointerCoords[0] = new MotionEvent.PointerCoords();
        pointerCoords[0].clear();
        pointerCoords[0].x = x;
        pointerCoords[0].y = y;
        pointerCoords[0].pressure = 1.0F;
        pointerCoords[0].size = 1.0F;
        MotionEvent motionEvent = MotionEvent.obtain(downTime, eventTime, action, 1, pointerProperties, pointerCoords,
                0, 0, 1.0F, yPrecision, 6, 0, InputDevice.SOURCE_TOUCHSCREEN, 0);
        motionEvent.setSource(source);

        try {
            injectInputEventMethod.invoke(inputManager, motionEvent, 0);
        } catch (Exception e) {
            e.printStackTrace();
        }
        motionEvent.recycle();
    }

    private static void injectKeyEvent(InputManager paramInputManager, Method injectInputEventMethod, KeyEvent keyEvent)
            throws InvocationTargetException, IllegalAccessException {
        injectInputEventMethod.invoke(paramInputManager, keyEvent, 0);
    }

    /**
     * @param deltaTime 25ms - 150ms
     */
    private static void sendClickEvent(InputManager inputManager, Method injectInputEventMethod,
                                       float x, float y, long deltaTime) {
        long time = SystemClock.uptimeMillis();
        try {
            injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                    MotionEvent.ACTION_DOWN, time, time, x, y, 1.0F);
            injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                    MotionEvent.ACTION_UP, time, time + deltaTime, x, y, 1.0F);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void sendKeyEvent(InputManager inputManager, Method injectInputEventMethod, int source, int code, boolean shift) {
        long time = SystemClock.uptimeMillis();
        int metaShiftOn = shift ? KeyEvent.META_SHIFT_ON : 0;
        try {

            KeyEvent keyEvent = new KeyEvent(time, time, MotionEvent.ACTION_DOWN, code,
                    0, metaShiftOn, -1, 0, 0, source);
            injectInputEventMethod.invoke(inputManager, keyEvent, 0);

            injectKeyEvent(inputManager, injectInputEventMethod, keyEvent);

            injectKeyEvent(inputManager, injectInputEventMethod,
                    new KeyEvent(time, time, MotionEvent.ACTION_UP, code, 0, metaShiftOn, -1, 0, 0, source));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    public static int getRotation() {
        try {
            return getWindowsManager().getRotation();
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        return -1;
    }

    @SuppressLint("PrivateApi")
    public static WebSocket.StringCallback getInputEventCallback() {
        if (sInputEventCallback == null) {
            synchronized (InputHelper.class) {
                if (sInputEventCallback == null) {
                    try {
                        @SuppressLint("DiscouragedPrivateApi")

                        Method method = InputManager.class.getDeclaredMethod(
                                "injectInputEvent", InputEvent.class, Integer.TYPE);

                        sInputEventCallback = createWebSocketHandler(method, getInputManager(), KeyCharacterMap.load(-1));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        return sInputEventCallback;
    }

    private static WebSocket.StringCallback createWebSocketHandler(final Method injectInputEventMethod,
                                                                   final InputManager inputManager,
                                                                   final KeyCharacterMap keyCharacterMap) {
//                                                        ,final IPowerManager paramIPowerManager) {
        return new WebSocket.StringCallback() {
            long downTime;
            boolean isDown;

            @Override
            public void onStringAvailable(String reqParam) {
                JSONObject paramJson;
                String eventType;
                float clientX;
                float clientY;
                try {
                    paramJson = new JSONObject(reqParam);
                    eventType = paramJson.getString("type");
                    clientX = (float) paramJson.optDouble("clientX");
                    clientY = (float) paramJson.optDouble("clientY");
                    if ("wakeup".equals(eventType)) {
//                        MainScreenShot.turnScreenOn(this.val$im, paramMethod, paramIPowerManager);
                        return;
                    }
                } catch (Exception e) {
                    Log.e("screenshotapp", "input websocket", e);
                    return;
                }
                if ("stop".equals(eventType)) {
                    System.exit(0);
                }

                if (doMouseAction(eventType, clientX, clientY, paramJson) ||
                        doKeyAction(eventType, paramJson) ||
                        doConfigureAction(eventType, paramJson) ||
                        doScreenRecord(eventType) ||
                        doShowToast(eventType, paramJson) ||
                        doTextInput(eventType, paramJson)) {
                    return;
                }

                if ("rotate".equals(eventType)) {
                    if (getRotation() == 0) {
//                        AdbRotationHelper.forceRotation(1);
                    } else {
//                        AdbRotationHelper.forceRotation(0);
                    }
                    return;
                }

                if ("scroll".equals(eventType)) {
                    long l = SystemClock.uptimeMillis();
                    MotionEvent.PointerProperties[] pointerProperties = new MotionEvent.PointerProperties[1];
                    pointerProperties[0] = new MotionEvent.PointerProperties();
                    pointerProperties[0].clear();
                    pointerProperties[0].id = 0;
                    MotionEvent.PointerCoords[] pointerCoords = new MotionEvent.PointerCoords[1];
                    pointerCoords[0] = new MotionEvent.PointerCoords();
                    pointerCoords[0].clear();
                    pointerCoords[0].x = clientX;
                    pointerCoords[0].y = clientY;
                    pointerCoords[0].pressure = 1.0F;
                    pointerCoords[0].size = 1.0F;
                    pointerCoords[0].setAxisValue(10, (float) paramJson.optDouble("deltaX"));
                    pointerCoords[0].setAxisValue(9, (float) paramJson.optDouble("deltaY"));
                    MotionEvent motionEvent = MotionEvent.obtain(l, l, MotionEvent.ACTION_SCROLL, 1, pointerProperties, pointerCoords,
                            0, 0, 1.0F, 1.0F, 0, 0, InputDevice.SOURCE_TOUCHSCREEN, 0);
                    try {
                        injectInputEventMethod.invoke(inputManager, motionEvent, 0);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    return;
                }
                Log.e("screenshotapp", "Unknown: " + paramJson);
            }

            public boolean doTextInput(String eventType, JSONObject paramJson) {
                if (paramJson != null && "text".equals(eventType)) {
                    if (mKeyCharacterMap == null) {
                        mKeyCharacterMap = KeyCharacterMap.load(KeyCharacterMap.VIRTUAL_KEYBOARD);
                    }
                    String content = paramJson.optString("text");
                    char[] chars = new char[content.length()];
                    content.getChars(0, content.length(), chars, 0);
                    KeyEvent[] events = mKeyCharacterMap.getEvents(chars);
                    try {
                        for (KeyEvent event : events) {
                            injectInputEventMethod.invoke(inputManager, event, 0);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
//                    KeyEvent event = new KeyEvent(SystemClock.uptimeMillis(),
//                            content, KeyCharacterMap.VIRTUAL_KEYBOARD, 0);
//                    try {
//                        if (Looper.getMainLooper() == null) {
//                            Looper.prepareMainLooper();
//                        }
//                        Method method = InputMethodManager.class.getDeclaredMethod("dispatchKeyEventFromInputMethod", View.class, KeyEvent.class);
//                        method.invoke(getInputMethodManager(), null, event);
//                    } catch (Exception e) {
//                        e.printStackTrace();
//                    }
                    return true;
                }
                return false;
            }

            public boolean doShowToast(String eventType, JSONObject paramJson) {
                if ("toast".equals(eventType)) {
//                    Intent intent = new Intent().setComponent(new ComponentName("com.koushikdutta.vysor", "com.koushikdutta.vysor.ToastReceiver"));
//                    intent.putExtra("toast", paramJson.optString("toast"));
////                    MainScreenShot.sendBroadcast(reqParam);
                    return true;
                }
                return false;
            }

            private boolean doScreenRecord(String eventType) {
                switch (eventType) {
                    case "start-recording":
//                        MainScreenShot.startRecording();
                        break;
                    case "stop-recording":
//                        MainScreenShot.stopRecording();
                        break;
                    default:
                        return false;
                }
                return true;
            }

            private boolean doMouseAction(String eventType, float x, float y, JSONObject paramJson) {
                switch (eventType) {
                    case "mousemove":
                        if (this.isDown) {
                            long eventTime = this.downTime + paramJson.optLong("deltaTime", SystemClock.uptimeMillis() - this.downTime);
                            injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                                    MotionEvent.ACTION_MOVE, this.downTime, eventTime, x, y, 1.0F);
                        }
                        break;
                    case "mouseup":
                        if (this.isDown) {
                            this.isDown = false;
                            long eventTime = this.downTime + paramJson.optLong("deltaTime", SystemClock.uptimeMillis() - this.downTime);
                            injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                                    MotionEvent.ACTION_UP, this.downTime, eventTime, x, y, 1.0F);
                        }
                        break;
                    case "mousedown":
                        if (!this.isDown) {
                            this.downTime = SystemClock.uptimeMillis();
                            this.isDown = true;
                            injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                                    MotionEvent.ACTION_DOWN, this.downTime, this.downTime, x, y, 1.0F);
                        }
                        break;
                    case "click":
                        if (!this.isDown) {
                            long deltaTime = paramJson.optLong("deltaTime", SystemClock.uptimeMillis() - this.downTime);
                            sendClickEvent(inputManager, injectInputEventMethod, x, y, deltaTime);
                        }
                        break;
                    case "drag":
                        if (!this.isDown) {
                            try {
                                JSONArray jsonArray = new JSONArray(paramJson.optString("path"));
                                Point startP = new Point(jsonArray.getInt(0), jsonArray.getInt(1));
                                Point endP = new Point(jsonArray.getInt(2), jsonArray.getInt(3));


                                this.downTime = SystemClock.uptimeMillis();
                                int timeStep = (int) (22 + 6 * Math.random());
                                long eventTime = downTime + timeStep;
                                //注入一个down事件
                                injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                                        MotionEvent.ACTION_DOWN, this.downTime, eventTime, startP.x, startP.y, 1.0F);
                                //构造一个贝塞尔曲线的控制点
                                PointF controlP = new PointF((3f * startP.x + endP.x) / 4, (startP.y + 3f * endP.y) / 4);
                                Path path = new Path();
                                //Path生成贝塞尔曲线
                                path.quadTo(controlP.x - startP.x, controlP.y - startP.y,
                                        endP.x - startP.x, endP.y - startP.y);
                                PathMeasure pathMeasure = new PathMeasure(path, false);
                                float length = pathMeasure.getLength();
                                int stepLen = 50;
                                float[] motionP = new float[]{0, 0};
                                //测量计算线上点的坐标，不断注入MOVE事件
                                for (int dist = 0; dist < length; dist += stepLen) {
                                    timeStep = (int) (20 + 6 * Math.random());
                                    eventTime += timeStep;
                                    pathMeasure.getPosTan(dist, motionP, null);
                                    float motionX = startP.x + motionP[0];
                                    float motionY = startP.y + motionP[1];
                                    try {
                                        Thread.sleep(timeStep - 5);
                                    } catch (InterruptedException e) {
                                        e.printStackTrace();
                                    }
                                    injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                                            MotionEvent.ACTION_MOVE, this.downTime, eventTime, motionX, motionY, 1.0F);
                                }
                                timeStep = (int) (22 + 6 * Math.random());
                                eventTime += timeStep;
                                //最后注入一个UP事件
                                injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                                        MotionEvent.ACTION_UP, this.downTime, eventTime, endP.x, endP.y, 1.0F);

                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                        break;
                    case "drag1":
                        if (!this.isDown) {
                            this.downTime = SystemClock.uptimeMillis();
                            try {
                                Log.d(TAG, "path: " + paramJson.optString("path"));
                                JSONArray jsonArray = new JSONArray(paramJson.optString("path"));
                                if (jsonArray.length() < 3) {
                                    Log.d(TAG, "doMouseAction: drag, jsonArray.length() < 3");
                                    return false;
                                }
                                JSONArray singlePoint = jsonArray.getJSONArray(0);
                                Float xx = Float.valueOf(singlePoint.getString(0));
                                Float yy = Float.valueOf(singlePoint.getString(1));
                                long deltaTime = 0;
                                Log.d(TAG, "doMouseAction: drag, ACTION_DOWN " + xx + ", " + yy + ", " + deltaTime);
                                injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN,
                                        MotionEvent.ACTION_DOWN, this.downTime, this.downTime, xx, yy, 1.0F);
                                for (int i = 1; i < jsonArray.length() - 1; i++) {
                                    Thread.sleep(deltaTime);
                                    singlePoint = jsonArray.getJSONArray(i);
                                    xx = Float.valueOf(singlePoint.getString(0));
                                    yy = Float.valueOf(singlePoint.getString(1));
                                    deltaTime = singlePoint.getLong(2);
                                    Log.d(TAG, "doMouseAction: drag, ACTION_MOVE " + xx + ", " + yy + ", " + deltaTime);
                                    injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN, MotionEvent.ACTION_MOVE,
                                            this.downTime, SystemClock.uptimeMillis(), xx, yy, 1.0F);
                                }
                                singlePoint = jsonArray.getJSONArray(jsonArray.length() - 1);
                                xx = Float.valueOf(singlePoint.getString(0));
                                yy = Float.valueOf(singlePoint.getString(1));
                                deltaTime = singlePoint.getLong(2);
                                Thread.sleep(deltaTime);
                                Log.d(TAG, "doMouseAction: drag, ACTION_UP " + xx + ", " + yy + ", " + deltaTime);
                                injectMotionEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_TOUCHSCREEN, MotionEvent.ACTION_UP,
                                        this.downTime, SystemClock.uptimeMillis(), xx, yy, 1.0F);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                        break;
                    default:
                        return false;
                }
                return true;
            }

            private boolean doKeyAction(String eventType, JSONObject paramJson) {

                if (sKeyCodeMap.containsKey(eventType)) {
                    sendKeyEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_KEYBOARD, sKeyCodeMap.get(eventType), false);
                    return true;
                }
                switch (eventType) {
                    case "keycode":
                        int keycode = paramJson.optInt("keycode");
                        sendKeyEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_KEYBOARD, keycode, paramJson.optBoolean("shift", false));
                        break;
                    case "keyevent":
                        int code = 0;
                        try {
                            code = (Integer) KeyEvent.class.getDeclaredField(paramJson.optString("keyevent")).get(null);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        sendKeyEvent(inputManager, injectInputEventMethod, InputDevice.SOURCE_KEYBOARD, code, paramJson.optBoolean("shift", false));
                        break;
                    case "keychar":
                        KeyEvent[] keyEvents = keyCharacterMap.getEvents(paramJson.optString("keychar").toCharArray());
                        if (keyEvents != null) {
                            try {
                                for (KeyEvent keyEvent : keyEvents) {
                                    injectKeyEvent(inputManager, injectInputEventMethod, keyEvent);
                                }
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                    default:
                        return false;
                }
                return true;
            }

            private boolean doConfigureAction(String eventType, JSONObject paramJson) {
                switch (eventType) {
                    case "bitrate":
//                    int bitrate = paramJson.optInt("bitrate", MainScreenShot.current.getBitrate(Integer.MAX_VALUE));
//                    if ((MainScreenShot.current != null) && (Build.VERSION.SDK_INT >= 19)) {
//                        MainScreenShot.current.setBitrate(i);
//                    }
                        break;
                    case "sync-frame":
//                    if ((MainScreenShot.current != null) && (Build.VERSION.SDK_INT >= 19)) {
//                        Log.i("screenshotapp", "creating sync frame");
//                        MainScreenShot.current.requestSyncFrame();
//                    }
                        break;
                    case "resolution":
//                        MainScreenShot.resolution = paramJson.optDouble("resolution", 0.0D);
//                        MainScreenShot.encodeSizeThrottle.postThrottled(null);
                        break;
                    case "displaySettings":
//                        MainScreenShot.setSizeAndDensity(paramJson);
//                        MainScreenShot.sendDisplayInfo();
                        break;
                    case "dimDisplay":
//                        MainScreenShot.dimDisplay(paramJson.optBoolean("dimDisplay", false));
                        break;
                    default:
                        return false;
                }
                return true;
            }

        };
    }
}
