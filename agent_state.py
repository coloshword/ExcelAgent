## agent_state: module defining the state of the agent
import pandas as pd 
from io import StringIO
import json

def get_file_obj(buffer, filename):
    '''
    gets the file object that represents the file 
    A file object is nothing more than a dictionary that contains <tab_name>, <df>
    If the input file is a csv, it will simply be a single entry dictionary with "tab_one" as the name 
    '''
    if filename.endswith('.csv'):
        ## read just the first df, and return it 
        # buffer has to be converted to stringio
        print("here is called")
        df = pd.read_csv(buffer)
        return {"tab_1": df}
    elif filename.endswith('.xlsx'):
        return pd.read_excel(buffer, sheet_name=None)
        

class AgentState:
        
    input_file = None 
    def __init__(self):
        with open('agent_instructions.json') as f:
            self.agent_instructions = json.load(f)
            self.messages=[
                    {"role": "system", "content": self.agent_instructions["react_base_prompt"]}, 
            ]
            self.chat_len = len(self.agent_instructions["react_base_prompt"])
    
    def add_message(self, role, message):
        self.chat_len += len(message)
        self.messages.append(
                {"role": role, "content": message}
        )

    def get_messages(self):
        return self.messages

    def add_file(self, buffer, filename):
        self.input_file = get_file_obj(buffer, filename)

    def is_task_defined(self):
        '''
        boolean function for whether or not the task is defined and ready to work 
        '''
        return self.input_file is not None
        ## some more advanced task outlining
