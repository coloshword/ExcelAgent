## auth.py
import secrets 
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from passlib.context import CryptContext 
from fastapi.security import OAuth2PasswordBearer
from models import User, UserInDB
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "some-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

token_exception = HTTPException (
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials, because of missing token cookie",
        headers={"WWW-Authenticate": "Bearer"},
    )

fake_users_db = {
    "aceroliang": {
        "username": "aceroliang",
        "full_name": "Acero Liang",
        "email": "acero.liangli@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

def verify_password(plain_password, hashed_password):
    """
    Verify a password against its hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generates a hash for a password..
    """
    return pwd_context.hash(password)

def get_user(db, username:str):
    """
    gets a user from the database
    """
    if username in db:
        user_dict = db[username] # db is going to be a dictionary
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username:str, password: str):
    """
    Checks if username and password are correct
    """
    user = get_user(fake_db, username)
    if not user:
        return False 
    if not verify_password(password, user.hashed_password):
        return False 
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

async def get_current_user(token: str = Depends(get_token_from_cookie)):
    """
    Get the current user from the JWT token.
    PROTECTED! by the JWT token! won't be given access until JWT token is given 
    """
    # create an exception to throw if credentials can't be verified 
    credentials_exception = HTTPException (
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # get the username from the JWT token 
    except JWTError:
        raise credentials_exception
    
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    simply an extra check to make sure the account isn't disabled. 
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user 