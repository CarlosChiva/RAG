#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel
import logging
logging.basicConfig(level=logging.INFO)
router = APIRouter()
class User(BaseModel):
    username: str
    password: str
class CollectionRequest(BaseModel):
    collection_name: str

#-------------------------Principal routes-----------------------
@router.get("/llm-response")
async def llm_response(input: str,
                        collection_name:str,
                        credentials  = Depends(credentials_controllers.verify_jws)
                        ):
    
    result = await controllers.querier(question=input,collection_name=collection_name,credentials=credentials)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    logging.info(f"type of result:{type(result)}")
    return result

@router.post("/add_document")
async def add_document(file: UploadFile = File(...),
                        name_collection: str = Form(...),
                        credentials  = Depends(credentials_controllers.verify_jws)
                        ):

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file")

    if not name_collection:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Collection name is required")

    try:
            data = await controllers.add_new_document_collections(file,name_collection,credentials)
            logging.info(f"type of data:{type(data)}")
            return {'data': data}
        
    except Exception as e:
            print(f"Error in process_pdf: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the PDF")

#-------------------------Collection routes-----------------------

@router.get("/collections")
async def get_collections_name(credentials  = Depends(credentials_controllers.verify_jws))->dict[str,list[str]]:

    collections= await controllers.show_name_collections(credentials)
    logging.info(f"type of collecitons:{type(collections)}")
    return {"collections_name": collections}

@router.get("/get-conversation")
async def get_conversation(collection_name,
                            credentials  = Depends(credentials_controllers.verify_jws)):

    collection_name=collection_name
    conversation=await controllers.get_conversation(collection_name,credentials)
    logging.info(f"type of conversation:{type(conversation)}")
    return conversation 

@router.post("/delete-collection")
async def delete_collection(collection: CollectionRequest,
                            credentials  = Depends(credentials_controllers.verify_jws)):

    collection_name=collection.collection_name
    await controllers.remove_collections(collection_name,credentials)
    logging.info(f"type of collection name:{type(collection_name)}")
    return {"collection_name deleted": collection_name}

