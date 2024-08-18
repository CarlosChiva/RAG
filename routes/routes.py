from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from fpdf import FPDF
router = APIRouter()

@router.get("/llm-response")
async def llm_response(input: str):
    result = await controllers.querier(input)

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
        pdf = FPDF()
        
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt=file.filename, ln=True, align='C')
        
        with NamedTemporaryFile(mode='w', delete=False, suffix='.pdf') as tmp_file:
            pdf.output(tmp_file.name)
            # Escriba los datos del archivo en el archivo temporal
            #pdf.write_pdf(tmp_file)
            
        data = await controllers.add_new_document_collections(name_collection,tmp_file.name)
        #print("Data extracted:", data)  # Depuración
        return {'data': data}
    except Exception as e:
        print(f"Error in process_pdf: {e}")
        return {'error': 'An error occurred while processing the PDF'}, 500

 