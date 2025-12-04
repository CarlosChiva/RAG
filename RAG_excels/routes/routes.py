from http.client import HTTPException
from fastapi import *
from controllers import controllers, credentials_controllers
from controllers.controllers import upload_file_controller, list_files_controller, get_file_controller, upload_file_edited_controller, websocket_handler
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
    return await upload_file_controller(file, credentials)

@router.get("/list_files")
async def list_files(credentials  = Depends(credentials_controllers.verify_jws)):
    """Method to list files saved 
    Args:
        credentials(JWT at header of request)
    Return: List with name of files saved """
    return await list_files_controller(credentials)

@router.get("/get_file")
async def get_file(name_file:str,credentials  = Depends(credentials_controllers.verify_jws)):
    """Method to get a file saved 
    Args:
        name_file(str): name of file to get. 
        credentials(JWT at header of request)
    Return: File saved """
    return await get_file_controller(name_file, credentials)

@router.post("/upload_file_edited")
async def upload_file_edited(file: UploadFile = File(...),credentials  = Depends(credentials_controllers.verify_jws)):
    """Method to list files saved 
    Args:
        credentials(JWT at header of request)
    Return: List with name of files saved """
    return await upload_file_edited_controller(file, credentials)

active_connections = {}

@router.websocket("/llm-query")
async def llm_response_websocket(websocket: WebSocket):
    """WebSocket handler for LLM queries"""
    await websocket_handler(websocket)
