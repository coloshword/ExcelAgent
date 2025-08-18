# models.py: stores the data structures 
from pydantic import BaseModel 
from typing import Optional 
from datetime import datetime

# User doesn't have the id field in db_init, since it's only used for internal indexing
class User(BaseModel):
    google_sub: str 
    email: str 
    created_on: datetime
    last_login: datetime

class UserInDB(BaseModel):
    id: str