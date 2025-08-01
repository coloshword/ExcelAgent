from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import auth

#ChatMessage: Object Model for a chat message. A ChatMessage can be either an attachment (base64 str) or message (str)
class ChatMessage(BaseModel):
    message: str | None
    attachment: str | None

origins = [
    "*"
]    

app = FastAPI()

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

'''
Endpoint for logging in and getting a 
'''

## following a quick auth guide 
@app.get("/")
async def root():
    return {"message": "FASTAPI Auth demo"}

# this should be a protected endpoint 
@app.get("/protected")
async def protected_route(current_user: str = Depends(auth.authenticate_user)):
    return {"message": f"Hello {current_user}, this is a protected route!"}

# login endpoint to get a jwt token 
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
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
    access_token = 