from model.rag_model import RagModel,DataBase
import os
from config import Config
import json
async def querier(question:str,conf:Config):

    database=DataBase(conf).get_database()
    result=RagModel().query(question,database)

    return result

async def get_configurations(user):
    try:
        conf_list=json.loads(os.getenv("CONFIG_FOLDER")+user+".json")
        configs=[conf.deserialize() for conf in conf_list]
        return configs
    except FileNotFoundError:
        # Si el archivo no existe, devolver una lista vacía
        return []
    except json.JSONDecodeError:
        # Si hay un error al decodificar JSON (archivo corrupto), devolver una lista vacía
        return []
async def add_configurations(user,conf:Config):
    try:
        # Construir la ruta del archivo JSON
        config_file = os.getenv("CONFIG_FOLDER") + user + ".json"
        
        # Verificar si el archivo existe
        if os.path.exists(config_file):
            # Si existe, cargar su contenido actual para agregar la nueva configuración
            with open(config_file, "r+") as f:
                data = json.load(f)
                # Agregar la nueva configuración al final
                data.append(conf.serialize())
                # Retroceder el cursor al inicio y sobrescribir el archivo
                f.seek(0)
                json.dump(data, f, indent=2)
        else:
            # Si no existe, crear una nueva lista con la primera configuración
            with open(config_file, "w") as f:
                json.dump([conf.serialize()], f, indent=2)
                
        return {"message": "Configuration added successfully"}
    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return {"error": str(e)}
