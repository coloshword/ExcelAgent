from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List

# lm_ops: functions for language model operations 
def make_LM_request(client:OpenAI, model: str, messages:List[dict]=[]):
    '''
    makes a language model request with past message history messages
        Params:
            client: the OpenAI client instance 
            model: the model to query 
            messages: the past messages 
    '''
    resp = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return dict(resp.choices[0].message)



def init_api_client() -> OpenAI:
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    return client 
