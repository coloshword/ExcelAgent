### test_agent: tests the agent 
from google import genai
from google.genai import types 
from server.agent import view_spreadsheet_declaration, execute_code_declaration, view_spreadsheet, execute_code
import json
import os 
from typing import List 

def test_agent_reason():
    input_grid = [['' for x in range(24)] for y in range(40)]
    user_request = "In the first column of the spreadsheet, include the 20 countries with the highest population"
    with open("./server/agent_config.json") as file:
        agent_config = json.load(file)

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    config = types.GenerateContentConfig(system_instruction=agent_config["agent_system_prompt"])

    contents = [
        types.Content(
            role="user", 
            parts=[types.Part(text=f"USER REQUEST: {user_request} | INSTRUCTIONS: {agent_config["agent_reason_prompt"]}")]
        ),
    ]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config
    )
    # add response to the agent_history
    contents.append(response.candidates[0].content)
    return contents 


def test_agent_act():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    contents = test_agent_reason()
    user_request = "In the first column of the spreadsheet, include the 20 countries with the highest population"
    with open("./server/agent_config.json") as file:
        agent_config = json.load(file)
    act_content = types.Content(
        role="user",
        parts=[types.Part(text=f"USER REQUEST: {user_request} |INSTRUCTIONS: {agent_config["agent_act_prompt"]}")]

    )
    tools = types.Tool(function_declarations=[view_spreadsheet_declaration, execute_code_declaration])
    config = types.GenerateContentConfig(system_instruction=agent_config["agent_system_prompt"], tools=[tools])
    contents.append(act_content)
    print(contents)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config
    )
    print(response)