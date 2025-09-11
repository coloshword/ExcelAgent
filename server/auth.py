## auth.py
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from fastapi.security import OAuth2PasswordBearer
from .models import User, PublicUser
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from psycopg2.pool import SimpleConnectionPool
from . import db_ops
from dotenv import load_dotenv
import os 
from pydantic import BaseModel
from .deps import get_pool

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
SECRET_KEY = os.environ.get("secret_key")

token_exception = HTTPException (
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials, because of missing token cookie",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_user(sub: str, pool:SimpleConnectionPool=Depends(get_pool)) -> BaseModel:
    """
    gets a user from the db, given the google_sub. Light wrapper of db_ops.get_user_with_sub()
        Params:
            pool: the pool to pull conns from
            sub: the google_sub of the user to get 
        Returns:
            user as models.User
    """
    user = db_ops.get_user_from_sub(sub, pool)
    return user
    

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token.
        Params:
            data: the dictionary to encode in jwt token (the payload)
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta # use timezone.utc for now() so all times are timezone aware (so changing timezones) doesn't affect the expiration time  
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # default set to 15 minutes 
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_token_from_cookie(request: Request):
    try: 
        return request.cookies.get("access_token")
    except KeyError:
        raise token_exception

async def get_current_user(pool: SimpleConnectionPool = Depends(get_pool), token: str = Depends(get_token_from_cookie)) -> PublicUser:
    """
    Endpoint for auth purposes. Returns either the PublicUser if authenticated properly, or throws a 401 unauthorized error
        Params:
            pool: The SimpleConnectionPool to pull connections from
            token: the auth token from the cookie (pulled from get_token_from_cookie
        Returns:
    """
    # create an exception to throw if credentials can't be verified 
    credentials_exception = HTTPException (
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("id") # get the google_sub (id) from the jwt
    except JWTError:
        raise credentials_exception
    user = get_user(sub, pool)
    if user is None:
        raise credentials_exception
    #public_user = PublicUser.model_validate(user.model_dump(include={'email'}))
    return user

def login_and_get_jwt(pool: SimpleConnectionPool, google_sub: str) -> str:
    '''
    handles logging in and gets the jwt, from the google sub
        Returns:
            pool: the SimpleConnectionPool to pull conns from
            jwt: the jwt 
    '''
    # update last login
    conn = pool.getconn()
    db_ops.update_last_login_time(conn, google_sub)
    data_dict = {
        "id": google_sub
    }
    jwt = create_access_token(data_dict) # default cookie with expires = 30 mins
    return jwt 

def handle_create_user_or_login(google_user_info: dict, pool: SimpleConnectionPool) -> str:
    '''
    handles create user or login. Either creates a new user in the db, or logs them in. Returns the jwt header  
        Params:
            google_user_info: the info pulled from google oath2
        Returns:
            jwt: the jwt of the newly logged in user 
    '''
    # see if user is in the db
    google_sub = google_user_info['id']
    if not db_ops.is_user_in_db(pool, google_sub):
        db_ops.create_user(pool, google_user_info)
    jwt = login_and_get_jwt(pool, google_sub)
    return jwt