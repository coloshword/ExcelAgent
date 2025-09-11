## db_ops: actual db operations 
import psycopg2
from psycopg2.pool import SimpleConnectionPool
import psycopg2.extensions
from dotenv import load_dotenv
import os 
from .models import User, Task, Sheet
import pydantic
from datetime import datetime
import base64
from typing import List
import pandas as pd 

'''
we should use SimpleConnectionPool, it's a process wide pool that contains
a set of database connections (con and cursor), so we don't need to 
create a new one per request
'''
def init_pool(min_connections: int, max_connections:int) -> SimpleConnectionPool:
    '''
    initiates a SimpleConnectionPool with min_connections, and max_connections
        Params:
            min_connections:
    '''
    load_dotenv()
    DB_config = {
        "db_name": os.getenv("db_name"),
        "user": os.getenv("user"),
        "host": os.getenv("host"),
        "port": os.getenv("port"),
        "password": os.getenv("password")
    }
    pool = SimpleConnectionPool(
        minconn= min_connections,
        maxconn=max_connections,
        dbname=DB_config["db_name"],
        user=DB_config["user"],
        password=DB_config["password"],
        host=DB_config["host"],
        port=DB_config["port"]
    )
    return pool

def build_insert_query_from_dict(d:dict, table:str, id_field_name:str) -> str:
    '''
    wrapper function to create an insert query from dictionary.
        Params:
            d: the dictionary representing the row to add. Make sure the dictionary keys match the table columns 
            table: the table name 
    '''
    # the number of placeholders is the length of d 
    # we need to specify the column names, which in this case will match the dictionary KEYS
    table_columns = list(d.keys())
    query = f"INSERT INTO {table} ({", ".join(table_columns)}) VALUES ({", ".join(['%s' for i in range(len(d))])}) RETURNING {id_field_name};"
    return query

def insert_model_to_table(model: pydantic.BaseModel, table:str, conn: psycopg2.extensions.connection, id_field_name:str):
    '''
    wrapper function to insert a model into a table. Does not do any checking of types or size of dictionary, make sure the parameters match.
        Params:
            d: the dictionary representing the row to add, make sure the dictionary keys match the table columns 
            table: the table name 
            conn: a connection from the SimpleConnectionPool
    '''
    cur = conn.cursor()
    # build the query 
    model_dict = model.model_dump()
    query = build_insert_query_from_dict(model_dict, table, id_field_name)
    # create the data (just a tuple of values)
    data = tuple(model_dict.values())
    cur.execute(query, data)
    created_id = cur.fetchone()[0]
    conn.commit()
    return created_id

def create_user(pool: SimpleConnectionPool, google_user_info: dict):
    '''
    creates a user in the database.
        Params:
            pool: the pool to get conns from 
            google_user_info: the google_user_info dictionary 
    '''
    conn = pool.getconn()
    try:
        user = {
            "google_sub": google_user_info["id"],
            "email": google_user_info["email"],
            "created_on": datetime.now(),
            "last_login": datetime.now()
        }
        # create a user object 
        #call the insert wrapper 
        insert_model_to_table(User(**user), 'users', conn, 'id')
    finally:
        pool.putconn(conn)

def create_task(pool: SimpleConnectionPool, google_sub:str):
    '''
    creates a task in the database
        Params:
            pool: the pool to get the conns from 
            google_sub: the google_sub of the user creating the task
    '''
    conn = pool.getconn()
    try:
        task = {
            "google_sub": google_sub,
            "last_activity_at": datetime.now()
        }
        task_id = insert_model_to_table(Task(**task), 'tasks', conn, 'task_id')
        return task_id
    finally:
        pool.putconn(conn)

def create_sheet(pool: SimpleConnectionPool, google_sub:str, task_id:int, filename:str, b64:str):
    '''
    creates a sheet in the database 
        Params:
            pool: the pool to get the conns from 
            google_sub: the google_sub of the user creating the sheet
            task_id: the task_id of the user creating the sheet
            filename: the filename of the associated sheet that the user submitted in the client,
            b64: file as b64
    '''
    # convert back to bytes 
    # string so convert back to ascii
    b64_bytes = b64.encode('ascii')
    file_as_bytes = base64.b64decode(b64_bytes)
    conn = pool.getconn()
    file_size = len(file_as_bytes)
    print(type(task_id))
    try: 
        sheet = {
            "task_id": task_id,
            "sheet_name": filename,
            "bytes": file_as_bytes,
            "size_bytes": file_size,
            "created_on": datetime.now()
        }
        insert_model_to_table(Sheet(**sheet), 'sheets', conn, 'sheet_id')
    finally: 
        pool.putconn(conn)

def update_last_login_time(conn: psycopg2.extensions.connection, google_sub: str):
    cur = conn.cursor()
    query = """
        UPDATE users 
        SET last_login = NOW()
        where google_sub = %s
    """
    cur.execute(query, (google_sub,))
    conn.commit()

def get_user_from_sub(sub:str, pool:SimpleConnectionPool) -> dict | None:
    '''
    gets the user given the sub
        Params:
            pool: the pool to get conns from
            sub: the google_sub of the user to get
    '''
    conn: psycopg2.extensions.connection = pool.getconn()
    cur: psycopg2.extensions.cursor = conn.cursor()
    try:
        query = '''
            SELECT * from users as u
            where u.google_sub = %s
        '''
        cur.execute(query, (sub,))
        rows:tuple = cur.fetchone()
        if rows:
            # to create a dictionary out of this zip the rows tuple, with the column names using cur.description
            columns = [desc[0] for desc in cur.description]
            d = dict(zip(columns, rows))
            return User(**d)
        else:
            return None
    finally:
        cur.close()
        pool.putconn(conn)


def is_user_in_db(pool:SimpleConnectionPool, sub:str) -> bool:
    '''
    Checks if the user has an existing account in the db 
        Params:
            pool: the pool to get conns from 
            sub: the google_sub of the user to check if they exist in the db
        Returns:
            True / False
    '''
    conn: psycopg2.extensions.connection = pool.getconn()
    cur: psycopg2.extensions.cursor = conn.cursor()
    try:
        query = '''
            SELECT * from users as u
            where u.google_sub = %s 
        '''
        cur.execute(query, (sub,))
        rows:tuple = cur.fetchone()
        if rows:
            return True
        else:
            return False 
    finally:
        cur.close()
        pool.putconn(conn)

def initialize_agent_state_in_db(pool: SimpleConnectionPool, messages: List[dict], sheet_state: pd.DataFrame):
    '''
    Creates an agent state in the database 
        Params:
            pool: the pool to get connections from
            messages: the initial state of the agent message history
            sheet_state: the dataframe representing the state of the sheet at request time
    '''
    query = """
    INSERT into agent_state (agent_messages, sheet_status)
    VALUES (%s, %s)
    returning agent_id
    """

if __name__ == "__main__":
    pool = init_pool(1, 10)