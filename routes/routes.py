from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
router = APIRouter()

@router.get("/llm-response")
async def llm_response(input: str):
    result = await controllers.user_input(input)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    
    return result
@router.post("/add_document")
async def add_document(file: UploadFile = File(...), name_collection: str = Form(...)):
    if not file.filename:# or not file.content_type.startswith('application/pdf'):
        return {'error': 'Invalid file'}, 400
    if not name_collection:
        return {'error': 'Collection name is required'}, 400
    
    try:
        print("File received:", file.filename)  # Depuración

        contents = await file.read()
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(contents)
            tmp.seek(0)
            temp_file_path = tmp.name 
            print("Temporary file path:", temp_file_path)  # Depuración

            data = controllers.add_new_document_collections(temp_file_path,name_collection)
            print("Data extracted:", data)  # Depuración

        return data

    except Exception as e:
        print(f"Error in process_pdf: {e}")
        return {'error': 'An error occurred while processing the PDF'}, 500

 