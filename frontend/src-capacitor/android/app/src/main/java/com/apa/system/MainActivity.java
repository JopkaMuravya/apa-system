package com.apa.system;

import android.content.pm.ApplicationInfo;
import android.os.Build;
import android.os.Bundle;
import android.webkit.WebView;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    // Способ 1: Предпочтительный (если BuildConfig доступен)
    // if (BuildConfig.DEBUG) {
    //    WebView.setWebContentsDebuggingEnabled(true);
    // }

    // Способ 2: Альтернативный
    if ((getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0) {
      WebView.setWebContentsDebuggingEnabled(true);
    }

    initializeWebViewSettings();
  }

  private void initializeWebViewSettings() {
    this.bridge.getWebView().post(() -> {
      WebView webView = this.bridge.getWebView();
      webView.getSettings().setJavaScriptEnabled(true);
      webView.getSettings().setAllowFileAccess(true);
      webView.getSettings().setAllowContentAccess(true);
      webView.getSettings().setAllowUniversalAccessFromFileURLs(true);
      webView.getSettings().setAllowFileAccessFromFileURLs(true);

      if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
        webView.getSettings().setMixedContentMode(
          android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        );
      }
    });
  }
}
