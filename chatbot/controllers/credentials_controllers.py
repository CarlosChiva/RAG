import hashlib
from typing import Union
from fastapi import Depends, HTTPException
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = os.getenv("ALGORITHM")
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token.startswith("Bearer "):  
        token = token.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.utcnow().timestamp() > payload["exp"]:
            raise HTTPException(status_code=401, detail="Token expired")
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e :
        raise HTTPException(status_code=401, detail=f"Invalid token {e} {payload}")
    
async def verify_jws(
    credentials: Union[HTTPAuthorizationCredentials, str] = Depends(security)
) -> str:

    try:
        # Manejar diferentes tipos de entrada
        if isinstance(credentials, HTTPAuthorizationCredentials):
            # Caso normal: viene de dependencia HTTP (GET/POST)
            token = credentials.credentials
        elif isinstance(credentials, str) and credentials.startswith("Bearer "):
            # Caso WebSocket: token ya viene con "Bearer "
            token = credentials.split("Bearer ")[1]
        elif isinstance(credentials, str):
            # Caso WebSocket: token sin "Bearer "
            token = credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials format")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
