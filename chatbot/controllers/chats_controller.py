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

async def get_conversation(credentials):
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
        await new_conversation("New_chat",credentials)
    return [data[credentials]]
async def new_conversation(collection_name,credentials):
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    if not credentials in data:
        data[credentials] = {} 
    data[credentials][collection_name]=[]
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)    

async def remove_conversation(chat_name,credendials):
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credendials].pop(chat_name.chatName)
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)
    return f"remove chat {chat_name} successfully"    