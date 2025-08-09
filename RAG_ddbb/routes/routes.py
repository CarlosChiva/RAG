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
from fastapi import WebSocket, WebSocketDisconnect

router = APIRouter()
class User(BaseModel):
    username: str
    password: str
class CollectionRequest(BaseModel):
    collection_name: str
active_connections = {}
import logging
logging.basicConfig(level=logging.INFO) 
#-------------------------Principal routes-----------------------
@router.websocket("/question")
async def llm_response(
                        websocket:WebSocket,
                        ):
       # Aceptar conexión
    await websocket.accept()
    
    # Registrar conexión
    connection_id = str(id(websocket))
    active_connections[connection_id] = websocket
    
    try:
        while True:
            try:
                # Recibir mensaje del cliente
                message_data = await websocket.receive_json()

                try:
                    await credentials_controllers.verify_jws(message_data.get("auth"))

                except HTTPException as e:
                    # Enviar error al cliente
                    error_response = {
                        "type": "error",
                        "message": e.detail,
                        "status_code": e.status_code
                    }
                    await websocket.send_text(json.dumps(error_response))
                    continue  # Continuar esperando más mensajes
                try:
                    input=message_data.get("question")
                    logging.info(f"Data recived: {message_data.get('config')}")
                    database_conf=Config(**message_data.get("config"))
                except Exception as e:
                    if websocket.client_state.CONNECTED:
                        await websocket.send_text(str(e))
                    continue
                try:

                    await controllers.querier(question=input,
                                              conf=database_conf,
                                              websocket=websocket
                                              )
                except Exception as e:
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
        active_connections.pop(connection_id, None)
        logging.info(f"Connection {connection_id} cleaned up")

@router.get("/get-list-configurations")
async def get_collections_name(credentials  = Depends(credentials_controllers.verify_jws)):
    result = await controllers.get_configurations(credentials)
    print("Return get_list_configurations  ",result)
    return result

@router.post("/add_configuration")
async def delete_collection(conf: Config,
                            credentials  = Depends(credentials_controllers.verify_jws)):
    
    result = await controllers.add_configurations(credentials,conf)
    return result

@router.get("/try-connection")  
async def try_connection(    
    connection_name: str = Query(...),
    type_db: str = Query(...),
    user: str = Query(...),
    password: str = Query(...),
    host: str = Query(...),
    port: str = Query(...),
    database_name: str = Query(...),credentials  = Depends(credentials_controllers.verify_jws)):
    conf = Config(
        connection_name=connection_name,
        type_db=type_db,
        user=user,
        password=password,
        host=host,
        port=port,
        database_name=database_name
    )
    result = await controllers.try_connection(conf)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    return {"message": "Conexión exitosa"}

@router.delete("/remove-configuration")
async def remove_conf(conf_rm:Config,
                                credentials  = Depends(credentials_controllers.verify_jws)):    
    result =await controllers.remove_configuration(conf_rm,credentials)    
    return {"Response":result}