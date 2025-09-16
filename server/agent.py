import time
import requests
from typing import List 
import json
from . import agent_helpers
from google import genai
import os 
## agent.py: defines the module that defines the agent behavior. It is important that all these functions are called 
# from celery

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open("./server/agent_config.json") as file:
    agent_config = json.load(file)

def agent_loop(agent_state_msg_history: List[dict], sheet_status: List[List[str]]):
    '''
    defines the main agentic loop
    agent loop: takes in agent_state_message_history: the current message history, in OpenAI api form
    also takes in the sheet_status. 
        Params:
            agent_state_msg_history: The message history of the agent 
            sheet_status: the status of the sheet currently
    '''
    task_done = False 
    next_step = 'Reason' # we update this to determine if we want to reason or if we want to act
    while not task_done:
        # call LM agent 
        if next_step == 'Reason':
            task_done = agent_reason(agent_state_msg_history, sheet_status)
            next_step = 'Act'
        else:
            task_done = agent_act(agent_state_msg_history, sheet_status)
            next_step = 'Reason'
            task_done = True
    return { 
        "agent_state_msg_history": agent_state_msg_history,
        "sheet_status": sheet_status
    }

def agent_reason(agent_state_msg_history: List[dict], sheet_status: List[List[str]]):
    '''
    Executes one step of reasoning. Note: modifies agent_state_msg_history in-place
        Params:
            - agent_state_msg_history: the current agent message history
            - sheet_status: the current_status of the sheet 
    '''
    

def agent_act(agent_state_msg_history: List[dict], sheet_status: List[List[str]]):
    '''
    Executes one step of reasoning. Note: modifies agent_state_msg_history in-place
        Params:
            - agent_state_msg_history: the current agent message history
            - sheet_status: the current_status of the sheet 
    '''
    pass 

## The section below defines specific tools 

# Defines a tool for the agent (function) to view the spreadsheet as a df
view_spreadsheet_declaration = {
    "name": "view_spreadsheet",
    "description": "View the spreadsheet the user has in front of them, in the form of a pandas dataframe",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}
def view_spreadsheet():
    print("you are viewing the spreadsheet")

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

def execute_code(code: str):
    print("You are executing code ")

if __name__ == "__main__":
    ## first thing would be to make a new agent state 
    ## create a 40 x 24 grid to represent input data 
    input_grid = [['' for x in range(24)] for y in range(40)]
    #user_request = "Please add the 10 countries with the highest population in the first column"
    user_request = "hello"
    # goal: return grid with this back to the frontend, making sure to use celery
    # mock the request 
    base = "http://127.0.0.1:8000"
    response = requests.post(base + '/agent_request', json= {
        "user_msg": user_request,
        "sheet_status": input_grid
    })
    print(response.status_code)
    task_id = response.json()["task_id"]
    # wait 
    time.sleep(3)
    task_response = requests.get(base + f'/tasks/{task_id}')
    print(task_response.json())