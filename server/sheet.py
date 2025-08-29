# sheet.py: defiens the backend functions relating to sheets 
import db_ops
from psycopg2.pool import SimpleConnectionPool

def create_sheet_in_db(pool:SimpleConnectionPool, google_sub:str, task_id, filename, b64):
    '''
    wrapper of db_ops.create_sheet
        Params:
            pool: the pool to get the conns from 
            google_sub: the google_sub of the user creating the sheet
            task_id: the task_id of the user creating the sheet
            filename: the filename of the associated sheet that the user submitted in the client 
    '''
    db_ops.create_sheet(pool, google_sub, task_id, filename, b64)
