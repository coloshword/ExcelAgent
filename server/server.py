from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from datetime import timedelta
from . import auth
from .models import User, PublicUser, ChatMessage, FileData, AgentRequest, TaskResultOut
import googleapiclient.discovery
from . import login_with_google
from .login_with_google import flow
import googleapiclient.discovery
from psycopg2.pool import SimpleConnectionPool
from contextlib import asynccontextmanager
from .deps import get_pool, get_lm_api_client
from openai import OpenAI
from . import db_ops
import json
from . import lm_ops
from . import sheet
from . import agent_helpers
from typing import List
from . import worker 
from celery.result import AsyncResult


class AddChat(BaseModel):
    text: str

class CreateSheetRequest(BaseModel):
    task_id: int
    attachments: list[FileData]

origins = [
    "http://127.0.0.1:5500"
]    

with open("config.json") as f:
    config = json.load(f)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = db_ops.init_pool(1, 10)
    app.state.llm_client = lm_ops.init_api_client()
    try:
        yield # yielding so that the function doesn't return until app lifespan ends
    finally:
        app.state.pool.closeall()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world():
    return "Hello world"

# endpoint that requires jwt token 
@app.get("/users/me", response_model=PublicUser)
async def read_users_me(current_user: User = Depends(auth.get_current_user)):
    """Get current user information."""
    public_user = PublicUser.model_validate(current_user.model_dump(include={'email'}))
    return public_user

# continue with google 
@app.get("/google")
async def continue_with_google_for_access_token():
    """
    Get JWT token with google authentication
    """
    auth_url, state = login_with_google.get_authorization_url()
    return RedirectResponse(auth_url)

@app.get("/google/auth/redirect")
def google_auth_redirect(req: Request, pool:SimpleConnectionPool = Depends(get_pool)):
    """
    The Google auth redirect, after the user "accepts" to login to the application
    Responsible for checking if auth is successful.
    """
    query_params = dict(req.query_params) # we can use this to get the status by checking if the 'code' value is there, has state, code, scope, authuser, prompt
    
    # Get the authorization code from the query parameters
    code = query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")
    
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials
        service = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute() # the user_info 
        redirect_url = f"{config['client_uri']}/agent.html"
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        jwt = auth.handle_create_user_or_login(user_info, pool)
        response.set_cookie(key="access_token", value=jwt, httponly=True, samesite="lax", secure=False, path="/")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

## endpoint to create an agent state 
@app.post("/agent_request", status_code=status.HTTP_201_CREATED)
def create_agent_state(agent_state:AgentRequest, pool:SimpleConnectionPool=Depends(get_pool)):
    '''
    creates the agent state. An agent state takes in the current state of the sheet to create it 
        Params:
            agent_state: the agent state payload object
            pool: the pool to take connections from 
    '''
    # initialize the worker task 
    # include the message history 
    # initialize one if not made 
    agent_message_history = agent_helpers.init_agent_message_history(agent_state.user_msg) 
    agent_state_id = db_ops.initialize_agent_state_in_db(pool, agent_message_history, agent_state.sheet_status)
    task = worker.make_agent_request.delay(agent_state.user_msg, agent_state.sheet_status)
    return {
        "agent_state_id": agent_state_id,
        "task_id": task.id
    }

@app.get("/tasks/{task_id}", response_model=TaskResultOut)
def get_task_status(task_id: str):
    '''
    gets the task_status of the celery worker (agent flow)
        Params:
            task_id: the task id
    '''
    task_result = worker.get_async_result(task_id)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }

    print("server result")
    print(result)
    return result 