import os 
from celery import Celery
from openai import OpenAI
from typing import List 
from . import agent 

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

@celery.task(name="make_lm_request")
def make_lm_request(agent_message_history: List[dict]):
    '''
    makes a request to the LLLM based on the current agent_message_history
        Params:
            agent_message_history: the agent message history in OpenAI API completions format
    '''
    client = OpenAI(
        api_key=os.environ.get("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages = agent_message_history
    )
    return dict(response.choices[0].message)['content']

@celery.task(name="make_agent_request")
def make_agent_request(user_request: str, sheet_status:List[List[str]]):
    '''
    celery wrapper for agent.agent_loop
        Params:
            user_request: the user request 
            sheet_status: the current status of the sheet 
    '''
    result = agent.agent_loop(user_request, sheet_status)
    return result

def get_async_result(id):
    '''
    wrapper to get the AsyncResult object from celery instance 
    '''
    return celery.AsyncResult(id)