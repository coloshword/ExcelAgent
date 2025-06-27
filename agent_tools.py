### agent_tools: module defining tools the agent can use 
import pandas as pd
import re

class AgentTools:

    def view_sheet(self, agent_state, sheet_name):
        '''
        allows you to see only the head and tail of the df 
        '''
        try:
            df = agent_state.input_file[sheet_name]
            head_tail_df = pd.concat([df.head(10), df.tail(10)])
            return head_tail_df.to_string()
        except KeyError:
            return "Your sheet name doesn't exist in the file, please try the tool again with a different sheet name"

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
