### functions for agentic purpose
from typing import List
import pandas as pd 

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

if __name__ == "__main__":
    pass