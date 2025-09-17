### functions for agentic purpose
from typing import List
import pandas as pd 
import requests 
import time 
from openai import OpenAI
import os 

def convert_sheet_array_to_df(grid: List[List[str]]):
    '''
    converts the 2d grid array into a dataframe 
        Params:
            grid: the 2d grid array
        Returns:
            df: the equivalent df  
    '''
    print(len(grid))
    column_names = [i for i in range(len(grid[0]))]
    df = pd.DataFrame(grid, columns=column_names)
    return df

def convert_df_to_sheet_array(df: pd.DataFrame):
    '''
    converts the df back into the 2d grid array
        Params:
            df: the pd.DataFrame represeenting the sheet
        Returns:
            sheet_array: the equivalent 2d sheet array
    '''
    sheet = [list(row[1:]) for row in df.itertuples()]
    return sheet

def init_agent_message_history(first_user_msg: str):
    '''
    initiates the agent message history, for the first user message, following OpenAI Chat Completions API
        ex: [{"role": "user", "content": 'Translate the following English text to French: "{text}"'}]

        first_user_msg: the first user message
    '''
    ## DEFINE SYS PROMPT HERE
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": first_user_msg
        }
    ]
    return messages

def make_lm_request(agent_message_history: List[dict]):
    '''
    makes a request to the LLLM based on the current agent_message_history
        Params:
            agent_message_history: the agent message history in OpenAI API completions format
    '''
    client = OpenAI(
        api_key=os.environ.get("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages = agent_message_history
    )
    return dict(response.choices[0].message)