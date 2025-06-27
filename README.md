# ExcelAgent
- Going to build an excel agent for working on microsoft excel / CSV automations.

05/31/25:
- First idea: 
    - 2 models: 
        - A planning model: (unknown). Breaks the task at hand into multiple different steps. First, it will get a set of COLUMN names from dataframes. 



06/04/25:
- goal is to choose the AI capable of planning enough to solve the problem
- another goal is to choose A setup, one that's capable `



- goal is to make a basic agent, that can automate very easy tasks but quickly
- So we will simply use the greedy algorithm, simply we are going to create the task and run it.

06/10/25:
--
goal: run the two models using llama cpp
- let's make a chat interface really quickly... 

06/12/25:
--
goal: once uploaded dataframe,

- define a very simple task, and have the LM write some code for it, return it and run the code on the dataframe  -- (works)

06/14/25:
--
include a chat area to provide a task for it to do, and have it run it...


06/17/25:
--
GOAL:
- attach a sheet, give it a task, and have it execute and output the download link back to you 
    - we can now attach a sheet 
    - now what we need to do is have it pass in the sheet along with some predefined instructions (let's have it have a separate instructions thread) 


06/21/25;
--
V2: Make it "translate queries", from user instructions to something the LLM can understand 


06/24/25:
--
--> V3 implementation: reAct style agent 

- first we need to define tools. Passing in an excel / csv sheet, we need to provide a way to see them
- we'll maintain an object style model for the inputs 
- so for state we probably want an agent_state class with a serries of stuff being kept A

- so for simplicity we will simply use a single file with multiple tabs. So we will start with input_file
- purely for siplest state, we want just one layer, and not add an unecessary layer with the original filename 
- so probably a dictionary, with:
- we will simply call it "file_obj" because its the object representing the file 
{
    tab_name: tab_df,
    tab_name: tab_df
}


06/25/25:
--
- we now have an AgentState, 
- we should define tools
- first, all tools will take in agent_state, that just makes sense 
- with the initial task, we will pass in the name of the sheets
- we have view sheets, now we just need to define some prompt that will tell it you can use 

06/26/25:
--
- now we have the sys prompt, let's get it to make a tool call
- the get_context function will provide the context (what sheets there are etc)... 
- ok now we have a json format 
