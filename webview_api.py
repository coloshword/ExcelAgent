### js api for webview 
import pandas as pd
from io import BytesIO
import base64

class WebviewAPI:
    
    dataframes = []

    def add_dataframe(self, b64):
        '''
        adds a dataframe 
        '''
        b64 = b64.split(',')[1]
        b64 = base64.b64decode(b64)
        buffer = BytesIO(b64)
        df = pd.read_excel(buffer)
        print(df)

