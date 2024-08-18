#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from fpdf import FPDF
import tempfile
import os

router = APIRouter()

@router.get("/llm-response")
async def llm_response(input: str):
  
    result = await controllers.querier(collection_name="first", question=input)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

    return result

@router.post("/add_document")
async def add_document(file: UploadFile = File(...), name_collection: str = Form(...)):

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
            data = await controllers.add_new_document_collections(name_collection, temp_path)
            return {'data': data}
        finally:
            os.unlink(temp_path)  # Asegura que el archivo temporal se elimine

    except Exception as e:
        print(f"Error in process_pdf: {e}")
        return {'error': 'An error occurred while processing the PDF'}, 500