from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import auth
from models import User

#ChatMessage: Object Model for a chat message. A ChatMessage can be either an attachment (base64 str) or message (str)
class ChatMessage(BaseModel):
    message: str | None
    attachment: str | None

origins = [
    "http://127.0.0.1:5500"
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

# login endpoint to get a jwt token 
@app.post("/token")
async def login_for_access_token(response: Response, request: Request, form_data: OAuth2PasswordRequestForm = Depends()): 
    """
    Authenticate user and return access token.
    """ 
    user = auth.authenticate_user(auth.fake_users_db, form_data.username, form_data.password)
    print(request.cookies)
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
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    """Get current user information."""
    return current_user

# this should be a protected endpoint 
@app.get("/protected")
async def protected_route(current_user: User = Depends(auth.get_current_active_user)):
    return {"message": f"Hello {current_user.full_name}, this is a protected route!"}