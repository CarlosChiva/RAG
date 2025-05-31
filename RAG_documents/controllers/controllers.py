from db.chroma_manager import add_pdf_to_collection,get_collections,add_pdf_to_collection, get_vectorstore,remove_collection_db
from db.chroma import get_chain
from db.model_conf import RagModel
from db.chroma_cli import get_chroma_client
import json
import os

PATH_CONVERSATIONS=os.getenv("PATH_CONVERSATIONS")
async def show_name_collections(credentials)->list[str]:

    cli=await get_chroma_client(credentials)
    return await get_collections(cli)
    

async def add_new_document_collections(document,name_collection,credentials)->dict[str,str]:
    
    cli=await get_chroma_client(credentials)
    return await add_pdf_to_collection(document,name_collection,cli)
   
async def remove_collections(collection_name,credentials)-> dict[str,str]:
    
    cli=await get_chroma_client(credentials)
    return await remove_collection_db(collection_name,cli)
  
async def querier(question:str,collection_name:str,credentials:str)->str:

    model=RagModel().get_model()

    cli=await get_chroma_client(credentials)
    vectorstore=await get_vectorstore(cli,collection_name)
    chain= await get_chain(model=model,vector_store=vectorstore)
    chat= await get_conversation(collection_name,credentials)
    
    response=chain.invoke({"input":question,"chat_history":chat})
    await add_conversation(collection_name,credentials,question,response['answer'])
    
    return response['answer']

async def add_conversation(collection_name,
                           credentials,
                           user_input,
                           bot_output)-> None:
    
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credentials][collection_name].append({"user":user_input})
    data[credentials][collection_name].append({"bot":bot_output})
    
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)
async def clear_conversation(collection_name,
                             credentials)->None:
    
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credentials][collection_name]=[]
    
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)

async def get_conversation(collection_name,credentials)->list[dict[str,str]]:
    
    if not os.path.exists(PATH_CONVERSATIONS):
        with open(PATH_CONVERSATIONS, "w") as f:
            json.dump({}, f)
    
    # Leer los datos existentes
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
   # Inicializar la estructura si no existe
    if credentials not in data:
        data[credentials] = {}
    
    if collection_name not in data[credentials]:
        data[credentials][collection_name] = []
        # Guardar los cambios
        with open(PATH_CONVERSATIONS, "w") as f:
            json.dump(data, f)
    return data[credentials][collection_name]

async def remove_conversation(collection_name,credentials)->None:
    
    # Leer los datos existentes
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
   
    if collection_name not in data[credentials]:
        data[credentials][collection_name] = []
        # Guardar los cambios
    with open(PATH_CONVERSATIONS, "w") as f:
        json.dump(data, f)
    return data[credentials][collection_name]