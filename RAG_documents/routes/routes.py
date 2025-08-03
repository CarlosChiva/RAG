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
class User(BaseModel):
    username: str
    password: str
class CollectionRequest(BaseModel):
    collection_name: str

#-------------------------Principal routes-----------------------
# Almacenar conexiones activas
active_connections = {}

@router.websocket("/llm-response")
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
                credentials = await credentials_controllers.verify_jws(websocket.headers.get("Authorization"))
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

@router.post("/add_document")
async def add_document(file: UploadFile = File(...),
                        name_collection: str = Form(...),
                        credentials  = Depends(credentials_controllers.verify_jws)
                        )->dict[str,dict[str,str]]:

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file")

    if not name_collection:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Collection name is required")

    try:
            data = await controllers.add_new_document_collections(file,name_collection,credentials)
            return {'data': data}
        
    except Exception as e:
            print(f"Error in process_pdf: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the PDF")

#-------------------------Collection routes-----------------------

@router.get("/collections")
async def get_collections_name(credentials  = Depends(credentials_controllers.verify_jws)
                               )->dict[str,list[str]]:

    collections= await controllers.show_name_collections(credentials)
    return {"collections_name": collections}

@router.get("/get-conversation")
async def get_conversation(collection_name,
                            credentials  = Depends(credentials_controllers.verify_jws)
                            )->list[dict[str,str]]:

    collection_name=collection_name
    return await controllers.get_conversation(collection_name,credentials)

@router.post("/delete-collection")
async def delete_collection(collection: CollectionRequest,
                            credentials  = Depends(credentials_controllers.verify_jws)
                            )->dict[str,str]:

    collection_name=collection.collection_name
    await controllers.remove_collections(collection_name,credentials)
    await controllers.remove_conversation(collection_name,credentials)
    return {"collection_name deleted": collection_name}

