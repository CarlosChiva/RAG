import os
from credentials_controllers import verify_jws
from fastapi import HTTPException, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import json
from models.agent import ExcelAgent

# Global variable to track active WebSocket connections
active_connections = {}

async def upload_file_controller(file: UploadFile = File(...), credentials: dict = None):
    """Method to save excel file
    Args:
        file(UploadFile): the excel file
        credentials(dict): JWT credentials from header
    Return : Message to confirmation of operation or error
    """
    try:
        # Create directory for user if not exists
        user_dir = os.path.join("user_files", credentials.get("user_id"))
        os.makedirs(user_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(user_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {"message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def list_files_controller(credentials: dict = None):
    """Method to list files saved 
    Args:
        credentials(dict): JWT credentials from header
    Return: List with name of files saved """
    try:
        user_dir = os.path.join("user_files", credentials.get("user_id"))
        if os.path.exists(user_dir):
            files = os.listdir(user_dir)
            return {"files": files}
        else:
            return {"files": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_file_controller(name_file: str, credentials: dict = None):
    """Method to get a file saved 
    Args:
        name_file(str): name of file to get. 
        credentials(dict): JWT credentials from header
    Return: File saved """
    try:
        user_dir = os.path.join("user_files", credentials.get("user_id"))
        file_path = os.path.join(user_dir, name_file)
        
        if os.path.exists(file_path):
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def upload_file_edited_controller(file: UploadFile = File(...), credentials: dict = None):
    """Method to list files saved 
    Args:
        credentials(dict): JWT credentials from header
    Return: List with name of files saved """
    try:
        # Create directory for user if not exists
        user_dir = os.path.join("user_files", credentials.get("user_id"))
        os.makedirs(user_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(user_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {"message": "File updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def websocket_handler(websocket: WebSocket):
    """Method to handle WebSocket connections and LLM queries"""
    agent=ExcelAgent() 

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
                credentials = await verify_jws(message_data.get("auth"))
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
            await agent.query(
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
