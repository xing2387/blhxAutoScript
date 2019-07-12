
package xxx.xxx.screenshotapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        findViewById(R.id.textview).setOnClickListener(this);

//        try {
//            JSONArray jsonArray = new JSONArray("[[555.0,1580.0,0], [555.0,1563.0,6], [555.0,1553.0,6], [555.0,1546.3616,20],[555.0,1543.0,7],[555.0,1531.0,8],[555.0,1516.0,10],[555.0,1514.5505,3],[555.0,1503.0,3], [559.0,1479.0,8], [559.0,1468.0,4], [559.8654,1460.211,3], [560.0,1459.0,7], [561.0,1450.0,4], [563.0,1441.0,5], [563.73,1437.7151,9], [563.73,1437.7151,5]]");
//
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        ArrayList<Float> xList = new ArrayList<>();
        ArrayList<Float> yList = new ArrayList<>();
        String events = ev.toString();
        if (ev.getHistorySize() > 0) {
//            StringBuilder sb = new StringBuilder();
//            sb.append(" [");
            for (int i = 0; i < ev.getHistorySize(); i++) {
//                sb.append(String.format(Locale.getDefault(), "(%f, %f),", ev.getHistoricalX(i), ev.getHistoricalY(i)));
                xList.add(ev.getHistoricalX(i));
                yList.add(ev.getHistoricalY(i));
            }
//            sb.replace(sb.length() - 1, sb.length() - 1, "]");
//            events = events.replace("historySize=" + ev.getHistorySize(), "historySize=" + ev.getHistorySize() + sb.toString());
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
