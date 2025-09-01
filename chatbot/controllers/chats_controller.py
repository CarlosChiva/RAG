import json
import os
import os
from dotenv import load_dotenv
from langgraph.graph import MessagesState
import logging
logging.basicConfig(level=logging.INFO)
load_dotenv()
PATH_CONVERSATIONS=os.getenv("PATH_CONVERSATIONS")
CONFIG_PATH=os.getenv("CONFIG_PATH")
CONFIGS_PATH=os.getenv("PATH_CONFIGS")

async def add_conversation(chat_name,credentials,user_input,bot_output):
    logging.info(f"----------Enter add_conversation------------")
    logging.info(f"user_input---{user_input}")
    logging.info(f"bot_output---{bot_output}")
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credentials][chat_name].append({"user":user_input})
    data[credentials][chat_name].append({"bot":bot_output})
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

async def remove_conversation(chat_name, credentials) -> str:
    # Read existing data
    with open(PATH_CONVERSATIONS, "r") as f:
        data = json.load(f)

    # Check if chat exists in user's conversations and delete it
    if chat_name in data[credentials]:
        del data[credentials][chat_name]

        # Save changes back to file
        with open(PATH_CONVERSATIONS, "w") as f:
            json.dump(data, f)
        return f"Conversation '{chat_name}' deleted successfully."

    return f"Conversation '{chat_name}' not found."
async def get_user_conversation(credentials: str, chat_name: str) -> list:
    if not os.path.exists(PATH_CONVERSATIONS):
        with open(PATH_CONVERSATIONS, "w") as f:
            json.dump({}, f)
    
    # Leer los datos existentes
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
   # Inicializar la estructura si no existe
    if credentials not in data.keys():
        data[credentials] = {}
    
    if chat_name not in data[credentials]:
        data[credentials][chat_name] = []
        # Guardar los cambios
        with open(PATH_CONVERSATIONS, "w") as f:
            json.dump(data, f)
    return data[credentials][chat_name]

async def update_name_chat(old_name,new_name,credendials)-> None:
    with open (PATH_CONVERSATIONS,"r") as f:
        data=json.load(f)
    data[credendials][new_name]=data[credendials].pop(old_name)
    with open (PATH_CONVERSATIONS,"w") as f:
        json.dump(data,f)
async def get_configurations(credentials)-> dict:
    if not os.path.exists(CONFIG_PATH):
        users_config={}
        users_config[credentials]={}
        with open(CONFIG_PATH, "w") as f:
            json.dump(users_config, f)

    with open (CONFIG_PATH,"r") as f:
        data=json.load(f)
    return data[credentials]







async def get_tools_configuration(credentials)-> dict:
    try:
        if not os.path.exists(CONFIGS_PATH):
            users_config={}
            users_config[credentials]={}
            with open(CONFIGS_PATH, "w") as f:
                json.dump(users_config, f)
                return users_config[credentials]
    except Exception as e:
        logging.error(f"Error getting configurations get_tools_configuration: {str(e)}")
    try:
        with open (CONFIGS_PATH,"r") as f:
            data=json.load(f)
        return data[credentials]
    except Exception as e:
        logging.error(f"Error getting configurations fail to read: {str(e)}")
        return {}


async def save_tools_conf(tools_conf,credendials):
    logging.info("saving....")
    try:
        if not os.path.exists(CONFIGS_PATH):
            with open(CONFIGS_PATH, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)

        logging.info(tools_conf)
        with open (CONFIGS_PATH,"r") as f:
            data=json.load(f)

        logging.info(data)
        if "image_tools" in tools_conf:

            if data[credendials].get("image_tools"):
                data[credendials]["image_tools"]=tools_conf["image_tools"]
            else:
                data[credendials]["image_tools"]={}
                data[credendials]["image_tools"]=tools_conf["image_tools"]
                
        elif "mcp_tools" in tools_conf:
            if data[credendials].get("mcp_tools"):
                data[credendials]["mcp_tools"]=tools_conf["mcp_tools"]
            else:
                data[credendials]["mcp_tools"]={}
                data[credendials]["mcp_tools"]=tools_conf["mcp_tools"]
           
        with open (CONFIGS_PATH,"w") as f:
            json.dump(data,f)
    except Exception as e:
        logging.error(f"Error saving configurations: {str(e)}")
    return True