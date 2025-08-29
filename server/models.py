# models.py: stores the data structures 
from pydantic import BaseModel 
from typing import Optional, List
from datetime import datetime

# User doesn't have the id field in db_init, since it's only used for internal indexing
'''
User: Model that defines a User internally, same as db
'''
class User(BaseModel):
    google_sub: str 
    email: str 
    created_on: datetime
    last_login: datetime

'''
Defines a Task
'''
class Task(BaseModel):
    google_sub: str
    last_activity_at: datetime

'''
Defines a sheet
'''
class Sheet(BaseModel):
    task_id: str
    sheet_name: str
    bytes: bytes 
    size_bytes: int
    created_on: datetime

'''
PublicUser: Model that defines a User exposed to the public
'''
class PublicUser(BaseModel):
    email: str    

class FileData(BaseModel):
    filename: str
    fileContent: str

class ChatMessage(BaseModel):
    text: str