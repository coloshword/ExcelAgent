### test_agent: tests the agent 
from google import genai
from google.genai import types 
from server.agent import view_spreadsheet_declaration, execute_code_declaration, view_spreadsheet, execute_code, init_agent_message_history, agent_reason, agent_act, agent_web_search
import json
import os 
from typing import List 
import server.agent2 as agent

def test_agent():
    user_request = "Can you add the first 20 biggest countries by population to the first column"

    sheet_state = [['' for x in range(24)] for y in range(40)]
    agent_obj = agent.Agent(user_request, sheet_state)

    agent_obj.agent_loop()