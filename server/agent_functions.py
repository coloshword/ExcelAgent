### functions for agentic purpose
from typing import List
import pandas as pd 

def convert_sheet_array_to_df(grid: List[List[str]]):
    '''
    converts the 2d grid array into a dataframe 
        Params:
            grid: the 2d grid array
        Returns:
            df: the equivalent df  
    '''
    print(len(grid))
    column_names = [i for i in range(len(grid[0]))]
    df = pd.DataFrame(grid, columns=column_names)
    return df

if __name__ == "__main__":
    pass