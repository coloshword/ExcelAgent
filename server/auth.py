## auth.py
import secrets 
from fastapi import Depends, FastAPI, HTTPException, status 
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from passlib.context import CryptContext 

SECRET_KEY = "some-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")