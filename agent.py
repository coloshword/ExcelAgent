## agent.py: the high level excel agent 
from openai import OpenAI
from agent_state import AgentState
from agent_tools import AgentTools
import utils


class ExcelAgent:
    client = OpenAI(
        api_key=
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    agent_state = AgentState()
    agent_tools = AgentTools()
    prev_called_tools = []
    

    def add_file_to_state(self, buffer, input_filename):
        '''
        when called adds a file to the agent_state 
        '''
        self.agent_state.add_file(buffer, input_filename)

    def send_task_LLM(self, messages):
        '''
        send_task_LLM: sends the task to the LLM 
        '''
        print(messages)
        rst = self.client.chat.completions.create(
                model="gemini-2.5-pro",
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

        while True:
            #print(self.agent_state.messages[-1]["content"]) 
            reply = self.send_task_LLM(self.agent_state.get_messages())
            if "Final Answer:" in reply:
                final_answer_txt = reply[len("Final Answer: "):]
                if 'run_code' in self.prev_called_tools:
                    # get the final agent_state input_file
                    final_file_content = utils.buffer_to_b64(utils.df_excel_obj_to_bytes(self.agent_state.input_file))
                    return {
                            "filename": "output.xlsx",
                            "content": final_file_content
                    }
                else:
                    print("this is false")
                    return final_answer_txt
            # else there is another tool call
            tool, params = self.agent_tools.parse_action(reply)
            self.prev_called_tools.append(tool)
            result = getattr(self.agent_tools, tool)(self.agent_state, **params)
            self.agent_state.add_message("assistant", reply)
            self.agent_state.add_message("system", f"Observation: {result}")
