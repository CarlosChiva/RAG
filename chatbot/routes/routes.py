#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel
from config import Config
import logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()    
class ChatItem(BaseModel):
    chatName: str
@router.post("/query")
async def query(config:Config,credentials  = Depends(credentials_controllers.verify_jws)
                        ):

    result = await controllers.query(credentials,config)
    logging.info(f"i: {result.content}")

    return result.content


@router.get("/get_ollama_models")
async def query(credentials  = Depends(credentials_controllers.verify_jws)
                        )-> list[dict]:

    result = await controllers.get_ollama_models()
    print("Return get_ollama_models  ",result)
    return result

@router.post("/new_chat")
async def query(chatName:ChatItem,credentials  = Depends(credentials_controllers.verify_jws)
                        )-> dict:

    result = await controllers.new_chat(credentials,chatName.chatName)
    
    return {"Response":result}

@router.get("/get_chats")
async def query(credentials  = Depends(credentials_controllers.verify_jws)
                        )-> dict[str,list[dict]]:

    result = await controllers.get_chats(credentials)
    logging.info(f"result: {result}")
    return {"collections_name":result}

@router.post("/remove-chat")
async def query(chatName:ChatItem,credentials  = Depends(credentials_controllers.verify_jws)
                        )-> dict:

    result = await controllers.remove_chat(chatName.chatName,credentials)
    return {"Response":result}
@router.get("/get-conversation")
async def query(chatName:str,credentials  = Depends(credentials_controllers.verify_jws)
                        )-> dict[str,list[dict]]:

    result = await controllers.get_conversation(credentials,chatName)
    logging.info(f"result: {result}")
    return {"collections_name":result}
