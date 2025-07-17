import re 

## code_executor: executes the python code from string, given an input and a string of file s
def strip_code_formatting(text):
    """
    Strips common code block formatting (```, ''', "", ') from a given string.

    Args:
        text: The input string potentially containing code formatting.

    Returns:
        The string with code formatting removed.
    """
    text = re.sub(r'^\s*```[a-zA-Z]*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?```\s*$', '', text, flags=re.MULTILINE)

    text = re.sub(r'^\s*"""\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?"""\s*$', '', text, flags=re.MULTILINE)

    text = re.sub(r"^\s*'''\n?", '', text, flags=re.MULTILINE)
    text = re.sub(r"\n?'''\s*$", '', text, flags=re.MULTILINE)

    text = re.sub(r"^\s*'\n?", '', text, flags=re.MULTILINE)
    text = re.sub(r"\n?'\s*$", '', text, flags=re.MULTILINE)

    text = re.sub(r'^\s*"\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?"\s*$', '', text, flags=re.MULTILINE)

    return text.strip()

def execute(code_str, input_df):
    '''
    high level wrapper for exec() that runs code_str cleaning it from llm output, and creating a dict of input_df 
    '''
    code_str_cleaned = strip_code_formatting(code_str)
    variables = {
            'input_df': input_df,
    }
    try:
        exec(code_str_cleaned, globals(), variables)
    except Exception as e:
        print(e)
    return variables['output_df']
