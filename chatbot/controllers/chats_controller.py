import json
import os
import os
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

async def get_conversation(collection_name,credentials):
        # Verificar si el archivo existe, si no, crearlo con un diccionario vacío
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
async def new_conversation(collection_name,credentials):
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credentials][collection_name]=[]
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)    