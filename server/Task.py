# task.py: defines the backend funtions relating to tasks
from . import db_ops
from psycopg2.pool import SimpleConnectionPool

def create_task_in_db(pool:SimpleConnectionPool, google_sub: str) -> int:
    '''
    creates the task in db. Wrapper of db_ops
    '''
    return db_ops.create_task(pool, google_sub)