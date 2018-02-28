
package xxx.xxx.screenshotapp;

import android.content.ComponentName;
import android.content.Context;
import android.content.ServiceConnection;
import android.hardware.display.DisplayManager;
import android.os.IBinder;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Display;
import android.view.WindowManager;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


    }
}
