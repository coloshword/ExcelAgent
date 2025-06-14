### js api for webview 
import pandas as pd
from io import BytesIO
import base64
from openai import OpenAI
import code_executor
import utils
import base64

class WebviewAPI:
    
    dataframe = None
    most_recent_request = ''
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="lm")

    def add_dataframe(self, b64):
        '''
        adds a dataframe 
        '''
        b64 = b64.split(',')[1]
        b64 = base64.b64decode(b64)
        buffer = BytesIO(b64)
        df = pd.read_excel(buffer)
        self.dataframe = df 
        output_b64 = self.test_execute_code()
        return {
                'status': 'success',
                'content': output_b64
                }

    def test_execute_code(self):
    
        simple_request = """
        Below is input_df:
        {dataframe}

        Access the dataframe using the variable input_df. input_df is of type dataframe. YOU ALREADY HAVE input_df, DONOT REDEFINE IT. ASSUME input_df is IN MEMORY. Given input_df, write PYTHON code (not a function) that adds a column called 'Ones', where the value for each cell is 1, as int. Please return ONLY VALID CODE, and code ONLY. At the end, define a variable called "output_df", which should be the output of the completed task. Make sure you have output_df. Output only code. 
        """.format(dataframe=self.dataframe.to_string())
        result = self.chat(simple_request)
        output_df = code_executor.execute(result, self.dataframe)
        # output_df is the dataframe to return 
        output_bytes = utils.df_to_excel_bytes(output_df)
        # convert output_bytes to b64
        bytes_content = output_bytes.getvalue()
        encoded_bytes = base64.b64encode(bytes_content).decode('utf-8')
        return encoded_bytes

    def chat(self, user_msg: str) -> str:
        """Return assistant reply as plain text."""
        rst = self.client.chat.completions.create(
            model="local",
            messages=[{"role": "user", "content": user_msg}],
            stream=False,
        )
        return rst.choices[0].message.content
