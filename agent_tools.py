### agent_tools: module defining tools the agent can use 
import pandas as pd
import re
import difflib
import code_executor

def _closest_sheet(sheets, name, cutoff=0.6):
    if name in sheets:
        return name
    best = max(
        sheets,
        key=lambda s: difflib.SequenceMatcher(None, s.lower(), name.lower()).ratio(),
    )
    score = difflib.SequenceMatcher(None, best.lower(), name.lower()).ratio()
    return best if score >= cutoff else None

class AgentTools:


    def view_sheet(self, agent_state, sheet_name, cutoff=0.6):
        """
        Return head/tail of the closest-matching sheet.
        Falls back to fuzzy match if exact name not found.
        """
        sheets = agent_state.input_file.keys()      

        if sheet_name in sheets:
            df = agent_state.input_file[sheet_name]
            return pd.concat([df.head(5), df.tail(5)]).to_string()

        best = max(
            sheets,
            key=lambda s: difflib.SequenceMatcher(None, s.lower(), sheet_name.lower()).ratio(),
        )
        score = difflib.SequenceMatcher(None, best.lower(), sheet_name.lower()).ratio()

        if score >= cutoff:         
            df = agent_state.input_file[best]
            return (
                f"(Interpreted sheet_name='{best}' - similarity {score:.2f})\n"
                + pd.concat([df.head(10), df.tail(10)]).to_string()
            )

        return "Your sheet name doesn't exist in the file; try a different name."

    def run_code(self, agent_state, sheet_name, code):
        """
        Execute arbitrary pandas code on a worksheet.

        Parameters
        ----------
        sheet_name : str
            Name (or fuzzy name) of the worksheet to load as `input_df`.
        code : str
            Python code that **must** create a variable `output_df`.
        """
        sheet = _closest_sheet(agent_state.input_file.keys(), sheet_name)
        if sheet is None:
            return (
                "No sheet matched that name (≥60 % similarity needed). "
                "Try again with a different sheet_name."
            )

        try:
            output_df = code_executor.execute(code, agent_state.input_file[sheet])
            print(output_df)
        except Exception as err:
            return f"RuntimeError: {type(err).__name__}: {err}"
        
        agent_state.input_file[sheet] = output_df
        preview = pd.concat([output_df.head(5), output_df.tail(5)]).to_string()
        return f"Success. Updated sheet '{sheet}'. Preview:\n{preview}"

    def interpret_LM_tool_call(self, lm_output):
        '''
        interprets the language model tool call. 
        Returns the output of the tool called, followed by a boolean flag, continue
        if continue is false, we assume the output is the answer 
        '''
        if "Final Answer" in lm_output:
            return "", False
        

    def parse_action(self, line: str):
        """
        Returns ("tool_name", {"param": "value", ...})
        """
        # split on the first 
        try:
            tool, arg_str = map(str.strip, line.split("|", 1))
        except ValueError:
            raise ValueError("No '|' found in action line")

        # split k=v pairs separated by ;
        args = {}
        for pair in re.split(r"\s*;\s*", arg_str):
            if not pair:
                continue
            k, v = map(str.strip, pair.split("=", 1))
            args[k] = v
        return tool, args
