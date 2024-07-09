
from db.saver import show_collections, add_documents_to_collection,search_name_collection
async def index():
    return {"message": "Hello World"}

async def new_collection(documents):
    maker= await create_new_collection(collection_name="first", pdf_path=documents)
    return maker

async def show_name_collections():
    names= await show_collections()
    return names
async def add_new_document_collections(collection_name,document):
    names= await add_documents_to_collection(collection_name,document)
    return names
