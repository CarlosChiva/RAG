from db.chroma_manager import add_pdf_to_collection,get_collections,add_pdf_to_collection,remove_collection_db
from db.chroma import get_chain
from db.model_conf import get_model
from db.mysql_manager import checker_users, registrer_users
from db.chroma_cli import get_chroma_client
import os


async def show_name_collections(credentials):
    cli=await get_chroma_client(credentials)
    print("User show_name_collections:",credentials)
    names= await get_collections(cli)
    return names

async def add_new_document_collections(document,cli):
    cli=await get_chroma_client(cli)

    names= await add_pdf_to_collection(document,cli)
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
    return await checker_users(user_name=user_name,password=password)

async def registrer(user_name:str,password:str):

    return await registrer_users(user_name=user_name,password=password)
    
