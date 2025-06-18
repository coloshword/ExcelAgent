### js api for webview 
import pandas as pd
from io import BytesIO
import base64
import code_executor
import utils
import base64
from agent import ExcelAgent

class WebviewAPI:
    agent = ExcelAgent()

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


    def chat(self, user_msg: str, input_file_b64=None, input_filename ='') -> str:
        """Return assistant reply as plain text."""
        if input_file_b64:
            b64 = base64.b64decode(input_file_b64)
            buffer = BytesIO(b64)
            df = pd.read_excel(buffer)
            self.agent.add_dataframe(input_filename, df)
        # start a task
        if self.agent.is_task_ready():
            print("creating task")
            result = self.agent.create_task(user_msg)
            return result
        else:
            print("not creating task")
        
        #rst = self.client.chat.completions.create(
        #    model="local",
        #    messages=[{"role": "user", "content": user_msg}],
        #    stream=False,
        #)
        #return rst.choices[0].message.content
