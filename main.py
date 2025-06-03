### main.py --starts the pywebview 
import webview
import webview_api
import frontend

api = webview_api.WebviewAPI()
html = frontend.html
window = webview.create_window('test window', js_api=api, html=html)
webview.start(debug=True)
