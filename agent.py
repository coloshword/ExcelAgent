## agent.py: the high level excel agent 
from openai import OpenAI
import code_executor
import utils
from agent_state import AgentState
from agent_tools import AgentTools
import json

class ExcelAgent:
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="lm")
    agent_state = AgentState()
    agent_tools = AgentTools()
    

    def add_file_to_state(self, buffer, input_filename):
        '''
        when called adds a file to the agent_state 
        '''
        self.agent_state.add_file(buffer, input_filename)

    def send_task_LLM(self, messages):
        '''
        send_task_LLM: sends the task to the LLM 
        '''
        rst = self.client.chat.completions.create(
                model="local",
                messages=messages,
                stream=False,
        )
        return rst.choices[0].message.content
    
    def get_context(self, sheet_names_lst, task):
        '''
        provides the context 
        '''
        context = """
        CONTEXT: HERE are the sheet_names in the excel sheet: {sheet_names}.
        ULTIMATE TASK: {task}
        """
        return context.format(sheet_names=sheet_names_lst, task=task)

    def run_task(self, user_msg): 
        sheet_names = list(self.agent_state.input_file.keys())
        task_msg = self.get_context(sheet_names, user_msg)
        self.agent_state.add_message("user", task_msg)

        str_output = self.send_task_LLM(self.agent_state.get_messages())
        # print output and see if it is valid json 
        # add output back to the state as "assistant"
        self.agent_state.add_message("assistant", str_output)
        # now we must run the code through an interpreter
        tool, params = self.agent_tools.parse_action(str_output)
        
        tool_output = getattr(self.agent_tools, tool)(self.agent_state, **params)
        # add 
        self.agent_state.add_message("tool", tool_output)
        str_output2 = self.send_task_LLM(self.agent_state.get_messages())
        print(str_output2)
        print(self.agent_state.messages)

