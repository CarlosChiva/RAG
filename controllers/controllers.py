from db.chroma_manager import add_pdf_to_collection,get_collections,add_pdf_to_collection
from db.chroma import get_chain
from db.model_conf import get_model
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
    #print("Controllers:",names)
    return names

async def querier(collection_name,question):
    model=get_model()
    chain= await get_chain(model=model,collection_name=collection_name)
    response=chain({"question":question})
    return response['answer']
