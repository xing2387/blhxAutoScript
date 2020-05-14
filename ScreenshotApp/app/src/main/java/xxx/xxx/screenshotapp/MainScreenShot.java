package xxx.xxx.screenshotapp;

import android.graphics.Bitmap;
import android.graphics.Point;
import android.os.Looper;
import android.util.Log;

import com.koushikdutta.async.AsyncServer;
import com.koushikdutta.async.http.NameValuePair;
import com.koushikdutta.async.http.server.AsyncHttpServer;
import com.koushikdutta.async.http.server.AsyncHttpServerRequest;
import com.koushikdutta.async.http.server.AsyncHttpServerResponse;
import com.koushikdutta.async.http.server.HttpServerRequestCallback;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.HashMap;
import java.util.Locale;

/**
 * 屏幕截图，
 * adb shell有特殊的权限可以调用一些私有api，包括截屏和发送输入事件。
 * <p>
 * adb shell 命令：
 * export CLASSPATH=/data/app/xxx.xxx.screenshotapp-2/base.apk    #将CLASSPATH指向apk文件
 * #或delvik的用这个 export CLASSPATH=/data/app/$(ls /data/app |grep xxx.screenshotapp)
 * exec app_process /system/bin xxx.xxx.screenshotapp.MainScreenShot '$@'
 * 转发端口 port 53516 for example
 * adb forward tcp:53516 tcp:53516
 * 浏览器访问： 127.0.0.1:53516/screenshot.jpg
 * <p>
 * <p>
 * adb shell "x=/data/app/$(ls /data/app|grep xxx.screenshotapp);if [[ -d $x ]] then export CLASSPATH=$x/base.apk; else export CLASSPATH=$x; fi;exec app_process /system/bin xxx.xxx.screenshotapp.MainScreenShot '$@'"
 * <p>
 * adb shell "x=/sdcard/Android/data/xxx.xxx.screenshotapp; if [[ ! -e $x ]] then mkdir $x;fi"
 * adb push classes.dex /sdcard/Android/data/xxx.xxx.screenshotapp/
 * adb shell "x=/sdcard/Android/data/xxx.xxx.screenshotapp; export CLASSPATH=$x/classes.dex; exec app_process $x xxx.xxx.screenshotapp.MainScreenShot '$@'"
 */
public class MainScreenShot {
    private static final String TAG = "MainScreenShot";

    private static final int PORT = 50087;

    private static ScreenshotHelper sScreenshotHelper;
    private static InputHelper sInputHelper;

    public static JSONObject reqParamToJson(AsyncHttpServerRequest request) {
        JSONObject jsonObject = new JSONObject();
        try {
            for (NameValuePair nameValuePair : request.getQuery()) {
                jsonObject.put(nameValuePair.getName(), nameValuePair.getValue());
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return jsonObject;
    }

    public static void main(String[] args) {

        sScreenshotHelper = new ScreenshotHelper();
        sInputHelper = new InputHelper();

        AsyncHttpServer httpServer = new AsyncHttpServer() {
            protected boolean onRequest(AsyncHttpServerRequest request, AsyncHttpServerResponse response) {
                return super.onRequest(request, response);
            }
        };

        Looper.prepare();
        System.out.println("Andcast MainScreenShot Entry!");

        AsyncServer server = new AsyncServer();
        httpServer.get("/stop", new HttpServerRequestCallback() {
            @Override
            public void onRequest(AsyncHttpServerRequest request, AsyncHttpServerResponse response) {
                response.send("MainScreenShot bye");
                System.exit(0);
            }
        });
        httpServer.get("/screenshot", new ScreenshotRequestCallback());
        httpServer.get("/size", new ScreenSizeRequestCallback());
        httpServer.get("/sendevent", new HttpServerRequestCallback() {
            @Override
            public void onRequest(AsyncHttpServerRequest request, AsyncHttpServerResponse response) {
                response.getHeaders().set("Access-Control-Allow-Origin", "*");
                String requestStr = reqParamToJson(request).toString();//request.getQuery().toString();
                response.send(requestStr);

//                System.out.println("/sendevent, " + requestStr);
                InputHelper.getInputEventCallback().onStringAvailable(requestStr);

            }
        });
        httpServer.listen(PORT);

        Looper.loop();
    }

    static class ScreenSizeRequestCallback implements HttpServerRequestCallback {

        private Point point = new Point();

        @Override
        public void onRequest(AsyncHttpServerRequest request, AsyncHttpServerResponse response) {
            try {
                response.getHeaders().set("Access-Control-Allow-Origin", "*");
                sScreenshotHelper.getCurrentDisplaySize(point);
                response.send(String.format(Locale.getDefault(),
                        "{ \"width\":%d , \"height\":%d }", point.x, point.y));
            } catch (Exception e) {
                response.code(500);
                response.send(e.toString());
            }
        }
    }

    static class ScreenshotRequestCallback implements HttpServerRequestCallback {

        private static final String PARAM_FORMAT = "format";        //String, in jpg/png/webp
        private static final String PARAM_QUALITY = "quality";      //int, in range [0,100]
        private static final String PARAM_SIZE = "size";            //int, in 480/540/720/1080
        private static final String PARAM_SCALE = "scale";          //int, in [0f,1f]

        private HashMap<String, Bitmap.CompressFormat> formatMap = new HashMap<String, Bitmap.CompressFormat>() {{
            put("jpg", Bitmap.CompressFormat.JPEG);
            put("png", Bitmap.CompressFormat.PNG);
            put("webp", Bitmap.CompressFormat.WEBP);
        }};

        public void onRequest(AsyncHttpServerRequest request, AsyncHttpServerResponse response) {
            try {

                JSONObject param = reqParamToJson(request);

                //图片格式
                String format = "jpg";
                if (param.has(PARAM_FORMAT)) {
                    format = param.getString(PARAM_FORMAT);
                }
                Bitmap.CompressFormat compressFormat = formatMap.get(format);
                if (compressFormat == null) {
                    compressFormat = Bitmap.CompressFormat.JPEG;
                }
                //压缩质量
                int quality = 100;
                if (param.has(PARAM_QUALITY)) {
                    quality = param.getInt(PARAM_QUALITY);
                }
                //图片大小
                int size;
                if (param.has(PARAM_SIZE)) {
                    size = param.getInt(PARAM_SIZE);
                    if (size > 0) {
                        sScreenshotHelper.setSize(size);
                    }
                }
                float scale;
                if (param.has(PARAM_SCALE)) {
                    scale = (float) param.getDouble(PARAM_SCALE);
                    if (scale > 0 || scale <= 1) {
                        sScreenshotHelper.setScale(scale);
                    }
                }

                long t = System.currentTimeMillis();
                Bitmap bitmap = sScreenshotHelper.screenshot();
//                System.out.println("sScreenshotHelper.screenshot() " + (System.currentTimeMillis() - t));
                ByteArrayOutputStream bout = new ByteArrayOutputStream();


                bitmap.compress(compressFormat, quality, bout);
                bout.flush();
                response.send("image/" + format, bout.toByteArray());
                bitmap.recycle();
//                System.out.println("Screenshot " + (System.currentTimeMillis() - t));

            } catch (Exception e) {
                response.code(500);
                response.send(e.toString());
                Log.e(TAG, "onRequest: ", e);
            }
        }
    }
}