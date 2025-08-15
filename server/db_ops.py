## db_ops: actual db operations 
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
import os 

'''
we should use SimpleConnectionPool, it's a process wide pool that contains
a set of database connections (con and cursor), so we don't need to 
create a new one per request
'''

def test_postgres_conn():
    conn = psycopg2.connect(
    )
    cur = conn.cursor()
    sample_query = """
    SELECT * from users
    """
    cur.execute(sample_query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.commit()
    cur.close()
    conn.close()

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
    conn = pool.getconn()
    print(conn)

if __name__ == "__main__":
    init_pool(1, 10)