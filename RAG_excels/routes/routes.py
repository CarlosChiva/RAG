#from tempfile import NamedTemporaryFile
from http.client import HTTPException
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel
from fastapi import WebSocket, WebSocketDisconnect
import json
router = APIRouter()

@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...),credentials  = Depends(credentials_controllers.verify_jws)):
    """Method to save excel file
    Args:
        file(UploadFile): the excel file
        Credentials(JWT at header of request)
    Return : Message to confirmation of operation or error
        """
        # Verify file 
        #
        # save file in direction using credentials (perhaps another parameter)
        #
        # return ok or error 
    pass

@router.get("/list_files")
async def list_files(credentials  = Depends(credentials_controllers.verify_jws)):
    """Method to list files saved 
    Args:
        credentials(JWT at header of request)
    Return: List with name of files saved """
        # search files
        #
        # return name of files found 
        
    pass

@router.get("/get_file")
async def get_file(name_file:str,credentials  = Depends(credentials_controllers.verify_jws)):
    """Method to get a file saved 
    Args:
        name_file(str): name of file to get. 
        credentials(JWT at header of request)
    Return: File saved """
        
        # search file
        #
        # return file 
        
    pass

@router.post("/upload_file_edited")
async def upload_file_edited(file: UploadFile = File(...),credentials  = Depends(credentials_controllers.verify_jws)):
    """Method to list files saved 
    Args:
        credentials(JWT at header of request)
    Return: List with name of files saved """
        
        # search files
        #
        # upgrade file
        # 
        # return message of state of operation 
        
    pass

active_connections = {}

@router.websocket("/llm-query")
async def llm_response_websocket(websocket: WebSocket):

    # Aceptar conexión
    await websocket.accept()
    
    # Registrar conexión
    connection_id = str(id(websocket))
    active_connections[connection_id] = websocket
    
    try:
        while True:
            # Recibir mensaje del cliente
            message_data = await websocket.receive_json()
            #message_data = json.loads(data)

            # Verificar credenciales (puedes reutilizar tu función existente)
            # Verificar credenciales
            try:
                credentials = await credentials_controllers.verify_jws(message_data.get("auth"))
            except HTTPException as e:
                # Enviar error al cliente
                error_response = {
                    "type": "error",
                    "message": e.detail,
                    "status_code": e.status_code
                }
                await websocket.send_text(json.dumps(error_response))
                continue  # Continuar esperando más mensajes
                        
            input_text = message_data.get("input")
            collection_name = message_data.get("collection_name")
            
            
            # Procesar la solicitud
            await controllers.querier(
                question=input_text,
                collection_name=collection_name,
                credentials=credentials,
                websocket=websocket
            )
            
            
            
    except WebSocketDisconnect:
        # Eliminar conexión cuando se desconecta
        if connection_id in active_connections:
            del active_connections[connection_id]
    except Exception as e:
        # Enviar error al cliente
        error_response = {
            "type": "error",
            "message": str(e)
        }
        await websocket.send_text(json.dumps(error_response))
        if connection_id in active_connections:
            del active_connections[connection_id]
