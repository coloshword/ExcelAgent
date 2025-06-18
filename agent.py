## agent.py: the high level excel agent 
from openai import OpenAI
import json

class ExcelAgent:
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="lm")
    # filenames: df body 
    dataframes = {
    }
    
    def __init__(self):
        # get the instructions 
        with open('agent_instructions.json') as f:
            self.agent_instructions = json.load(f)

    def create_task(self, user_request):
        '''
        Creates the prompt for the agent, given input_df, and user_request 
        '''
        # create the task 
        for filename, df in self.dataframes.items():
            input_df = df
        # now that we have input df, let's print the string of the head

        print(input_df.head().to_string())
        print(self.agent_instructions)

    def add_dataframe(self, filename, df):
        '''
        adds a dataframe to the excel agent 
        '''
        # we should do something if the filename is the same 
        self.dataframes[filename] = df

    def is_task_ready(self):
        '''
        helper function to check if is task ready. Checks if there are dataframes ready for example 
        '''
        return len(self.dataframes) > 0
        




