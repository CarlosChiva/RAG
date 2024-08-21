from db.chroma_manager import add_pdf_to_collection,get_collections,add_pdf_to_collection
from db.chroma import get_chain
from db.model_conf import get_model
import os
async def index():

    return {"message": "Hello World"}

async def new_collection(documents):

    maker= await add_pdf_to_collection(collection_name="first", pdf_path=documents)
    return maker

async def show_name_collections():

    names= await get_collections()
    return names

async def add_new_document_collections(document):

    names= await add_pdf_to_collection(document)
    #print("Controllers:",names)
    return names

async def querier(question:str):

    model=get_model()
    chain= await get_chain(model=model)
    response=chain.invoke({"input":question})

    return response['answer']
