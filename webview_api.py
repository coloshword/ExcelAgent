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
        # if there is an input_file, then we define 
        if input_file_b64:
            buffer = BytesIO(base64.b64decode(input_file_b64))
            self.agent.add_file_to_state(buffer, input_filename)
        
        if self.agent.agent_state.is_task_defined():
            self.agent.run_task(user_msg)
