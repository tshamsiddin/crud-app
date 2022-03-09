from fastapi import Depends, HTTPException
from . import schemas, database, models
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

secret_key="hello"
algorithm="HS256"
expire_minutes=30

def create_token(data:dict):
    to_encode =data.copy()
    expire=datetime.utcnow()+timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt= jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return encoded_jwt  

def verify_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token, secret_key, algorithms=algorithm)
        id: str=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str=Depends(oauth2_scheme), db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=401, detail="Could not validate", headers={"WWW-Authenticate": "Bearer"})
    token=verify_token(token, credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user