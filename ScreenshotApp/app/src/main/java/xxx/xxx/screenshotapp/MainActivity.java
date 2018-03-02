
package xxx.xxx.screenshotapp;

import android.content.ComponentName;
import android.content.Context;
import android.content.ServiceConnection;
import android.hardware.display.DisplayManager;
import android.os.IBinder;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Display;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;

import java.util.ArrayList;
import java.util.Locale;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        findViewById(R.id.textview).setOnClickListener(this);

    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        ArrayList<Float> xList = new ArrayList<>();
        ArrayList<Float> yList = new ArrayList<>();
        String events = ev.toString();
        if (ev.getHistorySize() > 0) {
            StringBuilder sb = new StringBuilder();
            sb.append(" [");
            for (int i = 0; i < ev.getHistorySize(); i++) {
                sb.append(String.format(Locale.getDefault(), "(%f, %f),", ev.getHistoricalX(i), ev.getHistoricalY(i)));
                xList.add(ev.getHistoricalX(i));
                yList.add(ev.getHistoricalY(i));
            }
            sb.replace(sb.length() - 1, sb.length() - 1, "]");
            events = events.replace("historySize=" + ev.getHistorySize(), "historySize=" + ev.getHistorySize() + sb.toString());
        }
        xList.add(ev.getX());
        yList.add(ev.getY());
        Log.d(TAG, events);
        Log.d(TAG, xList.toString());
        Log.d(TAG, yList.toString());
        Log.d(TAG, "=============");
        return super.dispatchTouchEvent(ev);
    }

    @Override
    public void onClick(View v) {

    }
}
