
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
        Log.d(TAG, ev.toString());
        return super.dispatchTouchEvent(ev);
    }

    @Override
    public void onClick(View v) {

    }
}
