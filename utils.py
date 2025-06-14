## utils
from io import BytesIO 

def df_to_excel_bytes(df):
    '''
    converts a dataframe to excel bytes
    '''
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    return buffer 

