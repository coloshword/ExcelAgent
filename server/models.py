# models.py: stores the data structures 
from pydantic import BaseModel 
from typing import Optional 
from datetime import datetime

class User(BaseModel):
    id: str
    google_sub: str 
    email: str 
    created_on: datetime
    last_login: datetime