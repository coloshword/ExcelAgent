from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from datetime import timedelta
import auth
from models import User
import googleapiclient.discovery
import login_with_google
from login_with_google import flow
import googleapiclient.discovery
from psycopg2.pool import SimpleConnectionPool
from contextlib import asynccontextmanager
from deps import get_pool
import db_ops


#ChatMessage: Object Model for a chat message. A ChatMessage can be either an attachment (base64 str) or message (str)
class ChatMessage(BaseModel):
    message: str | None
    attachment: str | None

origins = [
    "http://127.0.0.1:5500"
]    


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = db_ops.init_pool(1, 10)
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

'''
Endpoint for chatting with the LLM in the backend 
'''
@app.post("/chat")
async def add_message(msg: ChatMessage):
    return {"received_message": msg.message, "received_attachment": msg.attachment}

@app.get("/")
async def root():
    return {"message": "FASTAPI Auth demo"}

# login endpoint to get a jwt token 
@app.post("/token")
async def login_for_access_token(response: Response, request: Request, form_data: OAuth2PasswordRequestForm = Depends()): 
    """
    Authenticate user and return access token.
    """ 
    user = auth.authenticate_user(auth.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax", secure=False, path="/")
    return {"access_token": access_token, "token_type": "bearer"}

# endpoint that requires jwt token 
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_user)):
    """Get current user information."""
    return current_user

# this should be a protected endpoint 
#@app.get("/protected")
#async def protected_route(current_user: User = Depends(auth.get_current_active_user)):
#    return {"message": f"Hello {current_user.username}, this is a protected route!"}

# continue with google 
@app.get("/google")
async def continue_with_google_for_access_token():
    """
    Get JWT token with google authentication
    """
    auth_url, state = login_with_google.get_authorization_url()
    return RedirectResponse(auth_url)

@app.get("/google/auth/redirect")
async def google_auth_redirect(req: Request, response: Response, pool:SimpleConnectionPool = Depends(get_pool)):
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
        jwt = await auth.handle_create_user_or_login(user_info, pool)
        response.set_cookie(key="access_token", value=jwt, httponly=True, samesite="lax", secure=False, path="/")
        return {"message": "Authentication successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")