# Task: the class that defines a Task in python
import db_ops
from psycopg2.pool import SimpleConnectionPool

class Task:
    def __init__(self, pool: SimpleConnectionPool, google_sub:str):
        '''
        Creates a Task instance 
            Params:
                - google_sub: the google_sub of the user who created the task 
        '''
        self.create_task_in_db(pool, google_sub)

    def create_task_in_db(self, pool:SimpleConnectionPool, google_sub: str):
        '''
        creates the task in db. Wrapper of db_ops
        '''
        db_ops.create_task(pool, google_sub)
