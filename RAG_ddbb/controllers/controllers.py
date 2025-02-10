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
        conf_list=json.loads("Config_path"+user)
        configs=[conf.deserialize() for conf in conf_list]
        return configs
    except:
        return []
async def add_configurations(user,conf:Config):
    try:
        with open("Config_path"+user,"a") as f:
            f.write(json.dumps(conf.serialize()))
        return {"message":"Configuration added"}    
    except:
        return {"error":"Error adding configuration"}
