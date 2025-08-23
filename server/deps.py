from fastapi import Request 
from psycopg2.pool import SimpleConnectionPool
from openai import OpenAI

## module for dependencies 
def get_pool(request: Request) -> SimpleConnectionPool:
    '''
    get_pool dependency: function to handle getting pool. To be used in lifespan contextmanager 
        Params:
            request: the Request object of the function that uses the pool
        returns:
            pool to pull conns from
    '''
    return request.app.state.pool

def get_lm_api_client(request: Request) -> OpenAI:
    '''
    dependency to get the language model api client. To be used in lifespan context manager
        Params:
            request: the Request object of the function that uses the api_client
        returns:
            OpenAI client instance
    '''
    return request.app.state.llm_client