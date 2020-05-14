package xxx.xxx.screenshotapp;

import android.graphics.Bitmap;
import android.graphics.Point;
import android.os.Looper;

import com.koushikdutta.async.AsyncServer;
import com.koushikdutta.async.http.NameValuePair;
import com.koushikdutta.async.http.server.AsyncHttpServer;
import com.koushikdutta.async.http.server.AsyncHttpServerRequest;
import com.koushikdutta.async.http.server.AsyncHttpServerResponse;
import com.koushikdutta.async.http.server.HttpServerRequestCallback;

import org.json.JSONException;
import org.json.JSONObject;


public class MainControl {

    private static final int PORT = 50088;


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

        AsyncHttpServer httpServer = new AsyncHttpServer() {
            protected boolean onRequest(AsyncHttpServerRequest request, AsyncHttpServerResponse response) {
                return super.onRequest(request, response);
            }
        };

        Looper.prepare();
        System.out.println("Andcast MainControl Entry!");

        AsyncServer server = new AsyncServer();
        httpServer.get("/stop", new HttpServerRequestCallback() {
            @Override
            public void onRequest(AsyncHttpServerRequest request, AsyncHttpServerResponse response) {
                response.send("MainControl bye");
                System.exit(0);
            }
        });
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
        httpServer.listen(server, PORT);

        Looper.loop();
    }

}
