## utils
from io import BytesIO 
import base64

def df_to_excel_bytes(df):
    '''
    converts a dataframe to excel bytes
    '''
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer 

def buffer_to_b64(buffer):
    b64_str = base64.b64encode(buffer.read()).decode('utf-8')
    return b64_str 


