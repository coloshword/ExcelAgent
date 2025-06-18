# ExcelAgent
- Going to build an excel agent for working on microsoft excel / CSV automations.

15 mins left
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

    def test_execute_code(self):
    
        simple_request = """
        Below is input_df:
        {dataframe}

        Access the dataframe using the variable input_df. input_df is of type dataframe. YOU ALREADY HAVE input_df, DONOT REDEFINE IT. ASSUME input_df is IN MEMORY. Given input_df, write PYTHON code (not a function) that adds a column called 'Ones', where the value for each cell is 1, as int. Please return ONLY VALID CODE, and code ONLY. At the end, define a variable called "output_df", which should be the output of the completed task. Make sure you have output_df. Output only code. 
        """.format(dataframe=self.dataframe.to_string())
        result = self.chat(simple_request)
        output_df = code_executor.execute(result, self.dataframe)
        # output_df is the dataframe to return 
        output_bytes = utils.df_to_excel_bytes(output_df)
        # convert output_bytes to b64
        bytes_content = output_bytes.getvalue()
        encoded_bytes = base64.b64encode(bytes_content).decode('utf-8')
        return encoded_bytes
