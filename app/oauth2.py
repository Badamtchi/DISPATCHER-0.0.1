from jose import jwt, JWTError
from . import schemas
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # to create a tokan based on phone number as a user_id and expiration time
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    # to extract token and control it's credentials validation
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone: str = payload.get("user_id")
        if not phone:
            raise credentials_exception
        token_data = schemas.TokenData(phone=phone)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    # in any path operation takes the token from requests as a dependency and 
    # send it to verify_access_token
    credential_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", 
                                         headers={"WWW-Authenticate:": "Bearer"})
    return verify_access_token(token, credential_exception)
