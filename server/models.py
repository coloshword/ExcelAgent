# models.py: stores the data structures 
from pydantic import BaseModel 
from typing import Optional 

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None 

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str 

# model for google auth redirect 
class GoogleAuthRedirect(BaseModel):
    code: str
    client_id: str 
    client_secret: str
    redirect_uri: str
    grant_type: str 