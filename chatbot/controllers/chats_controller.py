import json
import os
import os
from dotenv import load_dotenv
load_dotenv()
PATH_CONVERSATIONS=os.getenv("PATH_CONVERSATIONS")
async def add_conversation(collection_name,credentials,user_input,bot_output):
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credentials][collection_name].append({"user":user_input})
    data[credentials][collection_name].append({"bot":bot_output})
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)
async def clear_conversation(collection_name,credentials):
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credentials][collection_name]=[]
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)

async def get_chats_list(credentials)->list[dict]:
        # Verificar si el archivo existe, si no, crearlo con un diccionario vacío
    if not os.path.exists(PATH_CONVERSATIONS):
        with open(PATH_CONVERSATIONS, "w") as f:
            json.dump({}, f)
    
    # Leer los datos existentes
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)

   # Inicializar la estructura si no existe
    if credentials not in data:
        data[credentials] = {"New_chat":[]}
    return [data[credentials]]
async def new_conversation(credentials,new_chat_name)->str:
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    if not credentials in data:
        data[credentials] = {} 
    data[credentials][new_chat_name]=[]
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)  
    return f"new chat {new_chat_name} created successfully"      

async def remove_conversation(chat_name,credendials)-> str:
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credendials].pop(chat_name)
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)
    return f"remove chat {chat_name} successfully"    
async def get_chat_conversation(credentials,chat_name)->list[dict[str,list[str]]]:
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    return data[credentials][chat_name]