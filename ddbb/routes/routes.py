#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
from pydantic import BaseModel
import logging

router = APIRouter()
class User(BaseModel):
    username: str
    password: str

@router.get("/log-in")
async def log_in(username: str, password: str):

    password_hashed = await credentials_controllers.generar_hash(password)

    result = await controllers.check_user(user_name=username, password=password_hashed)
    if not result:
        raise HTTPException(status_code=401, detail="User not found")
    
    token=await credentials_controllers.generate_token(password_hashed)
    logging.info(f"Token generated: {token}")
    return {"access_token": token}


@router.post("/sing_up")
async def delete_collection(data_user: User):
    
    password_hashed = await credentials_controllers.generar_hash(data_user.password)
    result =await controllers.registrer(user_name=data_user.username,password=password_hashed)
    
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token=await credentials_controllers.generate_token(password_hashed)
    logging.info(f"Token generated: {token}")
    return {"access_token": token}
