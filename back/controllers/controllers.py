from db.chroma_manager import add_pdf_to_collection,get_collections,add_pdf_to_collection,remove_collection_db
from db.chroma import get_chain
from db.model_conf import get_model
from db.mysql import checker_users, registrer_users
import os


async def show_name_collections():

    names= await get_collections()
    return names

async def add_new_document_collections(document):

    names= await add_pdf_to_collection(document)
    #print("Controllers:",names)
    return names

async def remove_collections():

    names= await remove_collection_db()
    #print("Controllers:",names)
    return names

async def querier(question:str):

    model=get_model()
    chain= await get_chain(model=model)
    response=chain.invoke({"input":question})

    return response['answer']
async def check_user(user_name:str,password:str):
    print("User:",user_name)
    print("Password:",password)
    return checker_users(user_name=user_name,password=password)

async def registrer(user_name:str,password:str):
    print("User:",user_name)
    print("Password:",password)
    return registrer_users(user_name=user_name,password=password)
    

