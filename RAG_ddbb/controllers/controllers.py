from model.rag_model import RagModel,DataBase
import os
from config import Config

async def querier(question:str,conf:Config):

    database=DataBase(conf).get_database()
    result=RagModel().query(question,database)

    return result

