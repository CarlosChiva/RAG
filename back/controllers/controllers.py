from db.chroma_manager import add_pdf_to_collection,get_collections,add_pdf_to_collection, get_vectorstore,remove_collection_db
from db.chroma import get_chain
from db.model_conf import RagModel
from db.mysql_manager import checker_users, registrer_users
from db.chroma_cli import get_chroma_client
import os

async def show_name_collections(credentials):
    cli=await get_chroma_client(credentials)
    print("User show_name_collections:",credentials)
    names= await get_collections(cli)
    return names

async def add_new_document_collections(document,name_collection,credentials):
    cli=await get_chroma_client(credentials)

    names= await add_pdf_to_collection(document,name_collection,cli)
    #print("Controllers:",names)
    return names

async def remove_collections(collection_name,credentials):
    cli=await get_chroma_client(credentials)
    names= await remove_collection_db(collection_name,cli)
    #print("Controllers:",names)
    return names

async def querier(question:str,collection_name:str,credentials:str):

    model=RagModel().get_model()

    cli=await get_chroma_client(credentials)
    vectorstore=await get_vectorstore(cli,collection_name)
    
    chain= await get_chain(model=model,vector_store=vectorstore)
    response=chain.invoke({"input":question})

    return response['answer']
async def check_user(user_name:str,password:str):
    return await checker_users(user_name=user_name,password=password)

async def registrer(user_name:str,password:str):

    return await registrer_users(user_name=user_name,password=password)
    
