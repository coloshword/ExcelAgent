### agent_tools: module defining tools the agent can use 
import pandas as pd
import re
import difflib

class AgentTools:


    def view_sheet(self, agent_state, sheet_name, cutoff=0.6):
        """
        Return head/tail of the closest-matching sheet.
        Falls back to fuzzy match if exact name not found.
        """
        sheets = agent_state.input_file.keys()      

        # 1. Exact match
        if sheet_name in sheets:
            df = agent_state.input_file[sheet_name]
            return pd.concat([df.head(10), df.tail(10)]).to_string()

        # 2. Fuzzy match (difflib ratio 0-1)
        best = max(
            sheets,
            key=lambda s: difflib.SequenceMatcher(None, s.lower(), sheet_name.lower()).ratio(),
        )
        score = difflib.SequenceMatcher(None, best.lower(), sheet_name.lower()).ratio()

        if score >= cutoff:             # e.g. 0.6 ≈ 60 %
            df = agent_state.input_file[best]
            return (
                f"(Interpreted sheet_name='{best}' - similarity {score:.2f})\n"
                + pd.concat([df.head(10), df.tail(10)]).to_string()
            )

        # 3. Nothing close enough
        return "Your sheet name doesn't exist in the file; try a different name."

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
