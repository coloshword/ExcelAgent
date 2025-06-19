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
            print("creating task")
            instructions = self.agent.create_task(user_msg)
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




        #output_code = self.send_task_LLM(instructions)
        #output_df = code_executor.execute(output_code, input_df)        
        ## output_df is what we want to turn into excel, give it the same name with --agent changed. 
        #print(output_df)
        #output_file = {
        #        filename: output_filename,
        #        content: utils.buffer_to_b64(utils.df_to_excel_bytes(output_df))
        #}
        
