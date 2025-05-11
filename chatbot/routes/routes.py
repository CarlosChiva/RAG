#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel
from config import Config


router = APIRouter()    
@router.post("/query")
async def query(query:str,config:Config,credentials  = Depends(credentials_controllers.verify_jws)
                        ):

    result = await controllers.query(query,credentials,config)
    return {"result":result}


@router.get("/get_ollama_models")
async def query(credentials  = Depends(credentials_controllers.verify_jws)
                        )-> list[dict]:

    result = await controllers.get_ollama_models()
    print("Return get_ollama_models  ",result)
    return result