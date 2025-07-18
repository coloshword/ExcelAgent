import subprocess, atexit, json, pathlib
import webview                         
from openai import OpenAI              
import time
import webview_api


if __name__ == "__main__":
    webview.settings['ALLOW_DOWNLOADS'] = True
    webview.create_window(
            title="Excel Agent",
            url="static/index.html",
            js_api= webview_api.WebviewAPI(),
            width=480,
            height=600,
    )
    webview.start(debug=True)


