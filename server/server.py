from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from datetime import timedelta
import auth
from models import User, PublicUser, ChatMessage, FileData
import googleapiclient.discovery
import login_with_google
from login_with_google import flow
import googleapiclient.discovery
from psycopg2.pool import SimpleConnectionPool
from contextlib import asynccontextmanager
from deps import get_pool, get_lm_api_client
from openai import OpenAI
import db_ops
import json
import lm_ops
import task
import sheet
from typing import List


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
        print(redirect_url)
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        jwt = auth.handle_create_user_or_login(user_info, pool)
        response.set_cookie(key="access_token", value=jwt, httponly=True, samesite="lax", secure=False, path="/")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

# create a sheet endpoint 
@app.post("/sheet")
def create_sheet(payload: CreateSheetRequest, user: User=Depends(auth.get_current_user), pool:SimpleConnectionPool=Depends(get_pool)):
    google_sub = user.google_sub
    task_id = payload.task_id
    print(type(task_id))
    # for now just create one sheet with the first attachemnt 
    attachments = payload.attachments
    attachment:FileData = attachments[0]
    filename: str = attachment.filename
    b64: str = attachment.fileContent
    sheet.create_sheet_in_db(pool, google_sub, task_id, filename, b64)

# create a task endpoint
@app.post("/task")
def create_task(user: User=Depends(auth.get_current_user), pool:SimpleConnectionPool=Depends(get_pool)):
    google_sub = user.google_sub
    return task.create_task_in_db(pool, google_sub)


@app.post("/chat") # add the current_user dependency to wall it off behind auth
async def chatWithLLM(user_msg: ChatMessage, client: OpenAI = Depends(get_lm_api_client), user: User = Depends(auth.get_current_user), pool:SimpleConnectionPool = Depends(get_pool)):
    # example response 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": user_msg.text
        }
    ]
    model = "gemini-2.5-flash"
    return lm_ops.make_LM_request(client, model, messages)