#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel


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
    
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name
    
        try:
            data = await controllers.add_new_document_collections(temp_path,name_collection,credentials)
            return {'data': data}
    
        finally:
            os.unlink(temp_path)  # Asegura que el archivo temporal se elimine

    except Exception as e:
        print(f"Error in process_pdf: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the PDF")

#-------------------------Collection routes-----------------------

@router.get("/collections")
async def get_collections_name(credentials  = Depends(credentials_controllers.verify_jws)):

    collections= await controllers.show_name_collections(credentials)
    return {"collections_name": collections}

@router.post("/delete-collection")
async def delete_collection(collection: CollectionRequest,
                            credentials  = Depends(credentials_controllers.verify_jws)):

    collection_name=collection.collection_name
    await controllers.remove_collections(collection_name,credentials)
    return {"collection_name deleted": collection_name}


# -------------------------------JWT routes-----------------------------

@router.get("/log-in")
async def log_in(username: str, password: str):

    password_hashed = await credentials_controllers.generar_hash(password)

    result = await controllers.check_user(user_name=username, password=password_hashed)
    if not result:
        raise HTTPException(status_code=401, detail="User not found")
    
    token=await credentials_controllers.generate_token(password_hashed)
    
    return {"access_token": token}


@router.post("/sing_up")
async def delete_collection(data_user: User):
    
    password_hashed = await credentials_controllers.generar_hash(data_user.password)
    result =await controllers.registrer(user_name=data_user.username,password=password_hashed)
    
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token=await credentials_controllers.generate_token(password_hashed)
    return {"access_token": token}
