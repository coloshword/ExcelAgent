## agent.py: the high level excel agent 
from openai import OpenAI
import json
import code_executor
import utils
from agent_state import AgentState
from agent_tools import AgentTools

class ExcelAgent:
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="lm")
    agent_state = AgentState()
    agent_tools = AgentTools()
    
    def __init__(self):
        # get the instructions 
        with open('agent_instructions.json') as f:
            self.agent_instructions = json.load(f)
            self.sys_prompt = self.agent_instructions["react_base_prompt"]
            print(self.sys_prompt)

    def add_file_to_state(self, buffer, input_filename):
        '''
        when called adds a file to the agent_state 
        '''
        self.agent_state.add_file(buffer, input_filename)

    def send_task_LLM(self, task):
        '''
        send_task_LLM: sends the task to the LLM 
        '''
        rst = self.client.chat.completions.create(
                model="local",
                messages=[{"role": "system", "content": "dee dee"}, {"role": "user", "content": task}],
                stream=False,
        )
        return rst.choices[0].message.content

    def run_task(self, user_msg): 
        print(user_msg)
        pass 



