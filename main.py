import subprocess, atexit, json, pathlib
import webview                         # pip install pywebview
from openai import OpenAI              # pip install openai==1.*
import time
import webview_api


# 20 mins left 
MODEL = pathlib.Path("qwen_coder/qwen2.5-coder-7b-instruct-q4_k_m.gguf")

LLAMA_CMD = [
    "./llama-server",
    "-m", str(MODEL),
    "--n-gpu-layers", "35"
]

llama = subprocess.Popen(LLAMA_CMD)
atexit.register(llama.terminate)
#time.sleep(7)
client = OpenAI(base_url="http://localhost:8080/v1", api_key="lm")


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


