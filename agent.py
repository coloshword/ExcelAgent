## agent.py: the high level excel agent 
from openai import OpenAI
import json
import code_executor
import utils

class ExcelAgent:
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="lm")
    # filenames: df body 
    dataframes = {
    }
    
    code_queue = [];
    
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
            output_filename = filename

        input_df_view = input_df.head().to_string()
        instruction_format = self.agent_instructions["basic_instruction1"]

        instructions = instruction_format.format(input_df_view=input_df_view, task=user_request)
        return instructions 

    def send_task_LLM(self, task):
        '''
        send_task_LLM: sends the task to the LLM 
        '''
        rst = self.client.chat.completions.create(
                model="local",
                messages=[{"role": "user", "content": task}],
                stream=False,
        )
        return rst.choices[0].message.content

    def add_code_to_queue(self, code_str):
        '''
        adds code to the queue to execute 
        '''
        self.code_queue.append(code_str)
    
    def execute_one_from_queue(self):
        '''
        executes one code snippet from the queue 
        '''
        snippet = self.code_queue[0] 
        self.code_queue.pop(0)
        input_filename = list(self.dataframes.keys())[0]
        input_df = self.dataframes[input_filename]
        output_df = code_executor.execute(snippet, input_df)
        # start a task
            #print("creating task")
            #instructions = self.agent.create_task(user_msg)
            #output_code = self.agent.send_task_LLM(instructions)
            #self.agent.add_code_to_queue(output_code)
        b64_str = utils.buffer_to_b64(utils.df_to_excel_bytes(output_df))
        # with_output_df, we now need to turn it into b64
        return {
                "filename": input_filename,
                "content": b64_str
        }

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

    def translate_user_query(self, user_query):
        '''
        given the user_query, it translates it to a prompt that the coding LLM can understand.  
        '''
        # get the view of input_df 
        for filename, df in self.dataframes.items():
            input_df = df
            output_filename = filename
        input_df_view = input_df.head().to_string()
        instruction_format = self.agent_instructions["translate_user_query_prompt"]
        instructions = instruction_format.format(view=input_df_view, query=user_query)
        # with instruction, send it to the llm
        return self.send_task_LLM(instructions)
