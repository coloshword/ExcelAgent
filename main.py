import subprocess, atexit, json, pathlib
import webview                         # pip install pywebview
from openai import OpenAI              # pip install openai==1.*
import time

# ---- 1. Start llama.cpp in server mode ------------------------------------
MODEL = pathlib.Path("phi_models/Phi-4-mini-instruct-Q4_K_M.gguf")
LLAMA_CMD = [
    "./llama-server",
    "-m", str(MODEL),
    "--n-gpu-layers", "35"
]

llama = subprocess.Popen(LLAMA_CMD)
atexit.register(llama.terminate)
time.sleep(7)

# ---- 2. OpenAI client pointed at local server -----------------------------
client = OpenAI(base_url="http://localhost:8080/v1", api_key="lm")

# ---- 3. Expose an API object to the frontend ------------------------------
class Api:
    def chat(self, user_msg: str) -> str:
        """Return assistant reply as plain text."""
        rst = client.chat.completions.create(
            model="local",
            messages=[{"role": "user", "content": user_msg}],
            stream=False,
        )
        return rst.choices[0].message.content

# ---- 4. Launch the window --------------------------------------------------
if __name__ == "__main__":
    webview.create_window(
        title="Excel Agent Chat",
        url="static/index.html",
        js_api=Api(),          # JS can call window.pywebview.api.chat(...)
        width=480,
        height=600,
    )
    webview.start()
