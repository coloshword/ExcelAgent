## agent loop rewrite 
from google.genai import types, Client 
import os 
from typing import List 
import pandas as pd
from . import agent_helpers
import json

client = Client(api_key=os.environ.get("GEMINI_API_KEY"))
with open("./server/agent_config.json") as file:
    agent_config = json.load(file)


## Agent implementation 
class Agent():
    sheet_df: pd.DataFrame
    is_finished: bool = False
    num_cycles: int = 0
    agent_msg_history: List[types.Content]
    current_step_type: str = 'Reason' ## the current step type being reason or act 
    finish_reason: str | None = ''
    tool_calls_by_name = []

    # Defines a tool for the agent (function) to view the spreadsheet as a df

    execute_code_declaration = {
        "name": "execute_code",
        "description": "Executes the code you provide in the tool call parameter. You are given a single input parameter, 'df' of type pandas.DataFrame. This is the dataframe representing the user's spreadsheet. By modifying this dataframe with your code, you can modify the user's spreadsheet. Do not redeclare 'df', it is given to you. Use it as if it has already been defined before.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code you want to execute"
                }
            },
            "required": ["code"],
        }
    }

    set_task_finished_declaration = {
        "name": "set_task_finished",
        "description": "Use this function to declare the task as finished. This must be called to end the agent loop. Once you call this function, the interaction ends. Call this function when the task is finished, and provide a finish_reason, which is the reason you are finished.",
        "parameters": {
            "type": "object",
            "properties": {
                "finish_reason": {
                    "type": "string",
                    "description": "The reason you are finished. Could be something like 'I added the <task>'"
                }
            },
            "required": ["finish_reason"],
        }
    }

    tools = types.Tool(function_declarations=[execute_code_declaration, set_task_finished_declaration])

    def __init__(self, user_request: str, sheet_status: List[List[str]]):
        self.sheet_df = agent_helpers.convert_sheet_array_to_df(sheet_status)
        self.user_request = user_request
        self.agent_msg_history = []

        self.act_config = types.GenerateContentConfig(
            system_instruction=agent_config["agent_system_prompt"], 
            tools=[self.tools], 
        )

    def agent_loop(self):
        '''
        defines the agent loop
        '''
        MAX_CYCLES = 10
        self.current_step_type = 'Act'
        while not(self.is_finished) and self.num_cycles < MAX_CYCLES:
            print(f"CYCLE {self.num_cycles}")
            self.agent_act()
            self.num_cycles += 1
        ## return the agent sheet state, as a list !
        sheet_state = agent_helpers.convert_df_to_sheet_array(self.sheet_df)
        return  {
            "sheet_status": sheet_state,
            "finish_reason": self.finish_reason
        }

    def agent_act(self):
        act_content = types.Content(
            role="user",
            parts=[types.Part(text=f"USER REQUEST: {self.user_request} | INSTRUCTIONS: {agent_config["agent_act_prompt"]} | The spreadsheet dataframe now looks like this {self.view_spreadsheet()}")]
        )
        self.agent_msg_history.append(act_content)
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=self.agent_msg_history,
            config=self.act_config 
        )
        if not resp.candidates:
            raise Exception(f"resp.candidates is None")
        # check for tool call
        # get the tool call 
        tool_call = resp.candidates[0].content.parts[0].function_call
        print(f'TOOL CALL {tool_call}')
        # first we should add the new status to the message history 
        self.agent_msg_history.append(resp.candidates[0].content)
        if tool_call and tool_call.name == "execute_code":
            print("Execute code called")
            print("assignment")
            ## we would probably try to execute the code, if there is an error append the error message to the history...
            try: 
                result: pd.DataFrame = self.execute_code(**tool_call.args)
                print("result was created")
                self.tool_calls_by_name.append("execute code")
                # no issue, update result.
                self.sheet_df = result 
            except Exception as e:
                # append error for the next run 
                self.agent_msg_history.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=f"There was an error in executing code| ERROR: {e}")]
                    )
                )
        elif tool_call and tool_call.name == "set_task_finished":
            self.tool_calls_by_name.append("set_task_finished")
            try:
                self.set_task_finished(**tool_call.args)
            except Exception as e:
                self.agent_msg_history.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=f"There was an error in executing code| ERROR: {e}")]
                    )
                )

    ## agent tools 
    def view_spreadsheet(self):
        return self.sheet_df.to_string()

    def execute_code(self, code:str): 
        '''
        Function to execute code 
            Params:
                code: the code to execute as a string 
        '''
        print("execute code")
        variables = {
            'df': self.sheet_df
        }
        print("here")
        exec(code, globals(), variables)
        return variables['df']

    def set_task_finished(self, finish_reason: str):
        '''
        sets the agent internal state to finished 
        '''
        self.is_finished = True
        self.finish_reason = finish_reason

