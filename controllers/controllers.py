from db.chroma_db import add_pdf_to_collection,get_collections,add_pdf_to_collection
async def index():
    return {"message": "Hello World"}

async def new_collection(documents):
    maker= await add_pdf_to_collection(collection_name="first", pdf_path=documents)
    return maker

async def show_name_collections():

    names= await get_collections()
    return names
async def add_new_document_collections(collection_name,document):
    names= await add_pdf_to_collection(collection_name,document)
    return names
