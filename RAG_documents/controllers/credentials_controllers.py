from typing import Union
from fastapi import Depends, HTTPException
import jwt
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = os.getenv("ALGORITHM")
security = HTTPBearer()
import logging
logging.basicConfig(level=logging.INFO)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)
                           )->str:
    token = credentials.credentials
    if token.startswith("Bearer "):  # Eliminar el prefijo si existe
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
    logging.info(f"----------Enter verify_jws------------")
    logging.info(f"credentials type: {type(credentials)}")
    logging.info(f"credentials value: {credentials}")
    
    try:
        # Manejar diferentes tipos de entrada
        if isinstance(credentials, HTTPAuthorizationCredentials):
            # Caso normal: viene de dependencia HTTP (GET/POST)
            token = credentials.credentials
            logging.info(f"Token from HTTPAuthorizationCredentials: {token}")
        elif isinstance(credentials, str) and credentials.startswith("Bearer "):
            # Caso WebSocket: token ya viene con "Bearer "
            token = credentials.split("Bearer ")[1]
            logging.info(f"Token from WebSocket with Bearer: {token}")
        elif isinstance(credentials, str):
            # Caso WebSocket: token sin "Bearer "
            token = credentials
            logging.info(f"Token from WebSocket direct: {token}")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials format")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
