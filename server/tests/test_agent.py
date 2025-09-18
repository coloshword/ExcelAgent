### test_agent: tests the agent 
from google import genai
from google.genai import types 
from server.agent import view_spreadsheet_declaration, execute_code_declaration, view_spreadsheet, execute_code, init_agent_message_history, agent_reason, agent_act
import json
import os 
from typing import List 

def test_agent_reason():
    input_grid = [['' for x in range(24)] for y in range(40)]
    user_request = "can you add the top 20 countries into the first column of the sheet"
    agent_msg_history = init_agent_message_history(user_request)
    # test agent_reason
    task_done, agent_state_msg_history = agent_reason(agent_msg_history, input_grid)
    assert len(agent_state_msg_history) == 2
    assert isinstance(agent_state_msg_history, list)
    assert isinstance(agent_state_msg_history[0], types.Content)

def test_agent_act():
    input_grid = [['' for x in range(24)] for y in range(40)]
    # first step is reasoning step 
    user_request = "Can you add the top 20 countries into the first column of the sheet"
    agent_msg_history = init_agent_message_history(user_request)
    task_done, agent_state_msg_history = agent_reason(agent_msg_history, input_grid)
    # call the agent_reason 
    task_done, agent_state_msg_history = agent_act(agent_state_msg_history, input_grid)
    assert len(agent_state_msg_history) == 4
    assert isinstance(agent_state_msg_history, list)
    assert isinstance(agent_state_msg_history[0], types.Content)