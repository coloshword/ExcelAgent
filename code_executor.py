## code_executor: executes the python code from string, given an input and a string of file s
def execute(code_str, input_df):
    '''
    high level wrapper for exec() that runs code_str cleaning it from llm output, and creating a dict of input_df 
    '''
    # do a str.replace pf ``` with ### 
    # ── clean wrapper markup ─────────────────────────────────────
    if code_str.lstrip().startswith("```"):
        code_str = "\n".join(code_str.splitlines()[1:-1])  

    if code_str.lstrip().startswith(('"""', "'''")):
        code_str = code_str.strip()[3:-3]
    print(code_str)
    # we need to pass in a dict with input_dfs
    variables = {
            'input_df': input_df,
    }
    try:
        exec(code_str, globals(), variables)
    except Exception as e:
        print(e)
    print("no issue running code")
    print(variables)
    return variables['output_df']
