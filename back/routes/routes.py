#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
import tempfile
import os
from pydantic import BaseModel

import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "tu_secreto_super_seguro"
ALGORITHM = "HS256"
security = HTTPBearer()

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
async def add_document(file: UploadFile = File(...), name_collection: str = Form(...)):
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
@router.get("/collections")
async def get_collections_name():
    collections= await controllers.show_name_collections()
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




class User(BaseModel):
    username: str
    password: str

import hashlib

def generar_hash(password):
    """
    Genera un hash para un password usando el algoritmo SHA-256.

    Args:
        password (str): El password a ser hashing.

    Returns:
        str: El hash generado.
    """
    # Convertir la contraseña a bytes
    password_bytes = password.encode('utf-8')

    # Crear un objeto SHA-256
    sha256 = hashlib.sha256()

    # Agregar los datos de la contraseña al flujo de hashing
    sha256.update(password_bytes)

    # Obtener el hash generado
    password_hash = sha256.hexdigest()

    return password_hash

def verify_jws(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@router.get("/log-in")
<<<<<<< Updated upstream
async def log_in(username:str,password:str):


    result =await controllers.check_user(user_name=username,password=password)
=======
async def log_in(username: str, password: str):
    print("Username:", username)
    print("Password (hashed):", generar_hash(password))

    # Llama a la función de verificación
    result = await controllers.check_user(user_name=username, password=generar_hash(password))
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Crear payload
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Expiración
        "iat": datetime.utcnow(),  # Fecha de emisión
    }

    # Firmar el token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token}
>>>>>>> Stashed changes


@router.post("/sing_in")
async def delete_collection(data_user: User):
    print("Data user:",data_user)

    result =await controllers.registrer(user_name=data_user.username,password=generar_hash(data_user.password))

    return {"collection_name deleted": result}