import time
import requests
from typing import List, Tuple 
from .models import AgentLoopOut
import json
from google.genai import types, Client
import os 
import pandas as pd
from . import agent_helpers

## agent.py: defines the module that defines the agent behavior. It is important that all these functions are called 
# from celery

client = Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open("./server/agent_config.json") as file:
    agent_config = json.load(file)

def init_agent_message_history(user_request: str) -> List[types.Content]:
    '''
    initiates the message history of the agent, from the first message, the user request. Note: the reasoning step is appeneded to this first message to trigger the first part of the agent_lop
        Params:
            user_request: the user request 
        Returns:
            agent_message_history in the form of a list of genai.types.Content
    '''
    contents = [
        types.Content(
            role="user", 
            parts=[types.Part(text=f"USER REQUEST: {user_request} | INSTRUCTIONS: {agent_config["agent_reason_prompt"]}")]
        ),
    ]
    return contents
     
def agent_loop(user_msg: str, sheet_status: List[List[str]]) -> dict:
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
    ## create the agent_message_history
    agent_state_msg_history = init_agent_message_history(user_msg)
    while not task_done:
        # call LM agent 
        if next_step == 'Reason':
            task_done, agent_state_msg_history, sheet_status = agent_reason(agent_state_msg_history, sheet_status)
            next_step = 'Act'
        else:
            task_done, agent_state_msg_history, sheet_status = agent_act(agent_state_msg_history, sheet_status)
            next_step = 'Reason'
    return {"sheet_status": sheet_status}


def agent_reason(agent_state_msg_history: List[types.Content], sheet_status: List[List[str]]) -> Tuple[bool, List[types.Content]]:
    '''
    Executes one step of reasoning. Note: modifies agent_state_msg_history in-place
        Params:
            - agent_state_msg_history: the current agent message history
            - sheet_status: the current_status of the sheet 
    '''
    # the first call is already reasoning  
    client = Client(api_key=os.environ.get("GEMINI_API_KEY"))
    # add  grounding ? 
    tools = types.Tool(google_search=types.GoogleSearch, function_declarations=[view_spreadsheet_declaration, execute_code_declaration])
    config = types.GenerateContentConfig(
        system_instruction=agent_config["agent_system_prompt"], 
        tools=[tools], 
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=agent_state_msg_history,
        config=config
    )
    # add response to the agent_history
    if response.candidates == None or response.candidates[0].content == None:
        print(response)
        raise Exception("None returned for reasoning step")
    print("agent_reason called") 
    agent_state_msg_history.append(response.candidates[0].content)
    return False, agent_state_msg_history, sheet_status


def agent_act(agent_state_msg_history: List[types.Content], sheet_status: List[List[str]]) -> Tuple[bool, List[types.Content]]:
    '''
    Executes one step of reasoning. Note: modifies agent_state_msg_history in-place
        Params:
            - agent_state_msg_history: the current agent message history
            - sheet_status: the current_status of the sheet 
    '''
    client = Client(api_key=os.environ.get("GEMINI_API_KEY"))
    act_content = types.Content(
        role="user",
        parts=[types.Part(text=f"INSTRUCTIONS: {agent_config["agent_act_prompt"]}")]
    )
    tools = types.Tool(google_search=types.GoogleSearch, function_declarations=[view_spreadsheet_declaration, execute_code_declaration])
    config = types.GenerateContentConfig(system_instruction=agent_config["agent_system_prompt"], tools=[tools])
    agent_state_msg_history.append(act_content)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=agent_state_msg_history,
        config=config
    )
    tool_call = response.candidates[0].content.parts[0].function_call
    ## actually call the tool
    if tool_call and tool_call.name == "execute_code":
        # add the sheet_status to the df 
        df = agent_helpers.convert_sheet_array_to_df(sheet_status)
        tool_call.args['df'] = df 
        result: pd.DataFrame = execute_code(**tool_call.args) # this is the resulting dataframe 
        sheet_status = agent_helpers.convert_df_to_sheet_array(result)
        agent_state_msg_history.append(response.candidates[0].content)
    return True, agent_state_msg_history, sheet_status

def agent_web_search(agent_state_msg_history: List[types.Content], sheet_status: List[List[str]]): 
    '''
    sample web search implementation
    just make a web search for now 
    include other tools to see if it works in conjunction
    '''
    client = Client(api_key=os.environ.get("GEMINI_API_KEY"))
    act_content = types.Content(
        role="user",
        parts=[types.Part(text=f"INSTRUCTIONS: {agent_config["agent_act_prompt"]}")]
    )
    tools = types.Tool(
        google_search=types.GoogleSearch(),
        function_declarations=[view_spreadsheet_declaration, execute_code_declaration]
    )
    config = types.GenerateContentConfig(system_instruction=agent_config["agent_system_prompt"], tools=[tools])
    agent_state_msg_history.append(act_content)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=act_content,
        config=config
    )
    tool_call = response.candidates[0].content.parts[0].function_call
    if tool_call.name == "execute_code":
        # add the sheet_status to the df 
        df = agent_helpers.convert_sheet_array_to_df(sheet_status)
        tool_call.args['df'] = df 
        #result: pd.DataFrame = execute_code(**tool_call.args) # this is the resulting dataframe 
        print(tool_call.args)
        result = None
    sheet_status = agent_helpers.convert_df_to_sheet_array(result)
    agent_state_msg_history.append(response.candidates[0].content)
    return True, agent_state_msg_history, sheet_status

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

def execute_code(code: str, df: pd.DataFrame):
    '''
    Function to execute code 
        Params:
            code: the code to execute as a string 
    '''
    variables = {
        'df': df
    }
    exec(code, globals(), variables)
    return variables['df']
