import ast
from model.rag_model import RagModel,DataBase
import os
from config import Config
import json
async def querier(question:str,conf:Config):

    database=DataBase(conf).get_database()
    result=RagModel().query(question,database)

    return result

async def get_configurations(user):
    print("Enter to get_configurations    ", user)
    try:
        print("file path  ",os.getenv("CONFIG_FOLDER")+user+".json")
        conf_list=os.getenv("CONFIG_FOLDER")+user+".json"
        with open(conf_list, "r") as f:
            conf_list = json.load(f)  
            print("Load json  ",conf_list)
            #conf_list=ast.literal_eval(conf_list)
            configs=[Config.deserialize(conf) for conf in conf_list]#[conf.deserialize() for conf in conf_list]
        return configs
    except FileNotFoundError as e:
        print("File not found", e)
        # Si el archivo no existe, devolver una lista vacía
        return []
    except json.JSONDecodeError as j:
        print("JSON decode error ", j )
        # Si hay un error al decodificar JSON (archivo corrupto), devolver una lista vacía
        return []
async def add_configurations(user,conf:Config):

    try:
        # Construir la ruta del archivo JSON
        config_file = os.getenv("CONFIG_FOLDER") + user + ".json"
        
        # Verificar si el archivo existe
        if os.path.exists(config_file):
                    # Si existe, cargar su contenido actual para agregar la nueva configuración
            with open(config_file, "r+") as f:  # Permite leer y escribir
                try:
                    data = json.load(f)  # Leer JSON existente
                except json.JSONDecodeError:
                    data = []  # Si el archivo está vacío o corrupto, inicializar lista vacía
                data.append(conf.serialize())  # Agregar nueva configuración
                f.seek(0)  # Volver al inicio del archivo para sobrescribirlo
                f.truncate()  # Eliminar el contenido anterior
                json.dump(data, f, indent=2)  # Escribir nuevo JSON correctamente
                return {"message": "Configuration added successfully"}
            
    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return {"error": str(e)}
async def try_connection(config):
    
    database=DataBase(config)
    return database.try_connect()
async def remove_configuration(conf_rm:Config,user):
    try:
        config_file = os.getenv("CONFIG_FOLDER") + user + ".json"

        # Verificar si el archivo existe y no está vacío
        if not os.path.exists(config_file) or os.stat(config_file).st_size == 0:
            return {"error": "Configuration file not found or empty"}

        # Leer el contenido actual del JSON
        with open(config_file, "r") as f:
            try:
                data = json.load(f)  # Cargar lista de configuraciones
            except json.JSONDecodeError:
                return {"error": "Invalid JSON format"}

        # Filtrar las configuraciones, eliminando la que coincida con `conf_to_delete`
        updated_data = [conf for conf in data if conf != conf_rm.dict()]

        # Si no se eliminó ninguna configuración, devolver mensaje de error
        if len(updated_data) == len(data):
            return {"error": "Configuration not found"}

        # Sobrescribir el archivo con la lista actualizada
        with open(config_file, "w") as f:
            json.dump(updated_data, f, indent=2)

        return {"message": "Configuration removed successfully"}

    except Exception as e:
        return {"error": str(e)}