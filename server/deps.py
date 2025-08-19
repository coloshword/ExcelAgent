from fastapi import Request 
from psycopg2.pool import SimpleConnectionPool

## module for dependencies 
'''
get_pool dependency: function to handle getting pool. To be used in lifespan contextmanager 
    Params:
        request: the Request object of the function that uses the pool
    returns:
        pool to pull conns from
'''
def get_pool(request: Request) -> SimpleConnectionPool:
    return request.app.state.pool