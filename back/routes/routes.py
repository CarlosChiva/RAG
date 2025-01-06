#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel


router = APIRouter()
async def set_collection_name(new_name):
    os.environ['COLLECTION_NAME'] = new_name    

#-------------------------Principal routes-----------------------
@router.get("/llm-response")
async def llm_response(input: str):
    print("Back Pregunta:  ",input)
    result = await controllers.querier(question=input)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    print("Back Respuesta:  ",result)
    return result

@router.post("/add_document")
async def add_document(file: UploadFile = File(...),
                        name_collection: str = Form(...),
                        credentials  = Depends(credentials_controllers.verify_jws)
                        ):
    current_collection=os.getenv("COLLECTION_NAME")
    if  current_collection!= name_collection:
        
        await set_collection_name(name_collection)
        print("Change collection name:", os.getenv("COLLECTION_NAME"))
    if not file.filename:
        return {'error': 'Invalid file'}, 400
    if not name_collection:
        return {'error': 'Collection name is required'}, 400
 
    try:
        print("File received:", file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name
        try:
            data = await controllers.add_new_document_collections(temp_path)
            return {'data': data}
        finally:
            os.unlink(temp_path)  # Asegura que el archivo temporal se elimine

    except Exception as e:
        print(f"Error in process_pdf: {e}")
        return {'error': 'An error occurred while processing the PDF'}, 500

#-------------------------Collection routes-----------------------

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
@router.get("/collections")
async def get_collections_name(credentials  = Depends(credentials_controllers.verify_jws)):

    collections= await controllers.show_name_collections(credentials)
    print("response:",collections)
    return {"collections_name": collections}
    

@router.get("/self-collection-name")
async def collection_name():

    return {"collection_name": os.getenv("COLLECTION_NAME")}



@router.post("/change-collection-name")
async def collection_name(collection_name: str = Form(...)):
    os.environ['COLLECTION_NAME'] = collection_name
    collection_name=os.getenv("COLLECTION_NAME")
    return {"collection_name": collection_name}

@router.post("/delete-collection")
async def delete_collection():
    collection_name=os.getenv("COLLECTION_NAME")
    await controllers.remove_collections()
    return {"collection_name deleted": collection_name}


# -------------------------------JWT routes-----------------------------
class User(BaseModel):
    username: str
    password: str


# Función para validar el JWT y extraer información del usuario


@router.get("/log-in")
async def log_in(username: str, password: str):
    print("Username:", username)
    password_hashed = await credentials_controllers.generar_hash(password)
    print("Password (hashed):", password_hashed)
    # Llama a la función de verificación
    result = await controllers.check_user(user_name=username, password=password_hashed)
    if not result:
        print("--------",result,"-------------")
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
