#from tempfile import NamedTemporaryFile
from http.client import HTTPException
import json
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel
from config import Config
import logging
logging.basicConfig(level=logging.INFO)
from fastapi import WebSocket, WebSocketDisconnect

router = APIRouter()    
class ChatItem(BaseModel):
    chatName: str
@router.websocket("/query")
async def query(websocket: WebSocket
                #config:Config,credentials  = Depends(credentials_controllers.verify_jws)
                        ):

    await websocket.accept()
    
    # Registrar conexión
    connection_id = str(id(websocket))
    
    try:
        while True:
            try:
                # Recibir mensaje del cliente
                message_data = await websocket.receive_json()
                logging.info(f"Data recived: {message_data}")

                message_data=Config(**message_data)
                logging.info(f"Data recived: {message_data.credentials}")

                try:
                    message_data.credentials =await credentials_controllers.verify_jws(message_data.credentials)

                except HTTPException as e:
                    # Enviar error al cliente
                    logging.info(f"Error credential: {e}")
                    error_response = {
                        "type": "error",
                        "message": e.detail,
                        "status_code": e.status_code
                    }
                    await websocket.send_text(json.dumps(error_response))
                    continue  # Continuar esperando más mensajes

                try:

                    logging.info(f"Data recived: {message_data}")
                   
                except Exception as e:
                    logging.info(f"Error credential: {e}")
                    if websocket.client_state.CONNECTED:
                        await websocket.send_text(str(e))
                    continue
                try:

                    await controllers.query(message_data,websocket)
                    
                except Exception as e:
                    logging.info(f"Error in query: {e}")
                    if websocket.client_state.CONNECTED:
                        await websocket.send_text(str(e))
                        
            except WebSocketDisconnect:
                # Cliente desconectado normalmente
                logging.info(f"Client disconnected: {connection_id}")
                break
                
    except Exception as e:
        # Solo enviar error si la conexión sigue activa
        try:
            if websocket.client_state.CONNECTED:
                await websocket.send_text(str(e))
                await websocket.close()
        except:
            # Si falla al enviar, simplemente logear
            logging.error(f"Failed to send error message: {e}")
    
    finally:
        # Limpiar conexión del registro
        logging.info(f"Connection {connection_id} cleaned up")


    # logging.info(f"i: {result.content}")

    # return result.content


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
    await controllers.remove_conversation(chatName.chatName,credentials)
    return {"Response":result}
@router.get("/get-conversation")
async def query(chatName:str,credentials  = Depends(credentials_controllers.verify_jws)
                        )-> list[dict[str,str]]:

    result = await controllers.get_conversation(credentials,chatName)
    logging.info(f"result: {result}")
    return result
class ChatItem(BaseModel):
    oldChatName: str
    newChatName: str

@router.post("/update-chat-name")
async def update_chat_name(chat_item: ChatItem, credentials=Depends(credentials_controllers.verify_jws)):
    try:
        await controllers.update_chat_name(chat_item.oldChatName, chat_item.newChatName, credentials)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating chat name: {str(e)}")
