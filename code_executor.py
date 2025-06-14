## code_executor: executes the python code from string, given an input and a string of file s
def execute(code_str, input_df):
    '''
    high level wrapper for exec() that runs code_str cleaning it from llm output, and creating a dict of input_df 
    '''
    # do a str.replace pf ``` with ### 
    code_str = code_str.replace('```', '#')
    # we need to pass in a dict with input_dfs
    variables = {
            'input_df': input_df,
    }
    exec(code_str, globals(), variables)
    return variables['output_df']

