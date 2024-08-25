#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
import tempfile
import os

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
