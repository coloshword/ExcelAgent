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

    def chat(self, user_msg: str, input_file_b64=None, input_filename ='') -> str:
        """Return assistant reply as plain text.
        Two level activity, we will return the code being run, and then have it trigger 
        """
        if input_file_b64:
            b64 = base64.b64decode(input_file_b64)
            buffer = BytesIO(b64)
            df = pd.read_excel(buffer)
            self.agent.add_dataframe(input_filename, df)
        # start a task
        if self.agent.is_task_ready():
            translated_user_prompt = self.agent.translate_user_query(user_msg)
            instructions = self.agent.create_task(translated_user_prompt)
            output_code = self.agent.send_task_LLM(instructions)
            self.agent.add_code_to_queue(output_code)
            return output_code
        else:
            print("not creating task")

    def execute_last_request(self):
        '''
        when called, executes the last request 
        '''
        return self.agent.execute_one_from_queue()

    def translate_user_request(self, user_msg: str, input_file_b64=None, input_filename=''):
        if input_file_b64:
            b64 = base64.b64decode(input_file_b64)
            buffer = BytesIO(b64)
            df = pd.read_excel(buffer)
            self.agent.add_dataframe(input_filename, df)

        output_code = self.agent.translate_user_query(user_msg)
        return output_code


