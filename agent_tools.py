### agent_tools: module defining tools the agent can use 
import pandas as pd

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

