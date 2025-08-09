from typing import Literal
from fastapi import HTTPException
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
from enums_type import Enumms as ennum
from config import Config
load_dotenv()
from sqlalchemy import create_engine
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
from langchain_core.runnables import RunnablePassthrough

class DataBase:
    def __init__(self,conf:Config):
        try:
            self.driver = self.extract_driver(conf.type_db)
            self.user = conf.user
            self.password = conf.password
            self.host = conf.host
            self.port = conf.port
            self.database_name = conf.database_name
            self.database_url = f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"
            self.connect_db()
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al inicializar la base de datos: {e}")

    def extract_driver(self,type_db)-> Literal["sqlite", "mysql+pymysql", "postgresql+psycopg2"]:
        
        match type_db:
            case ennum.SQLITE.value:
                return "sqlite"
            case ennum.MYSQL.value:
                return "mysql+pymysql"
            case ennum.POSTGRESQL.value:
                return "postgresql+psycopg2"
            case _:
                raise ValueError(f"Invalid database type: {type_db}")
    def get_database(self):
        return self.database
    def get_engine(self):
        return create_engine(self.database_url)
    def try_connect(self)->dict:
        try:
            engine = create_engine(self.database_url)
        except Exception as e:
            return {"success": False, "error": f"No se pudo crear el motor de conexión: {str(e)}"}
        try:
            with engine.connect():
                pass
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": f"No se pudo conectar con la base de datos: {str(e)}"}

    def connect_db(self):
        try:
            self.database = SQLDatabase.from_uri(self.database_url)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"No se pudo conectar a la base de datos: {e}")


class SQLQueryParser(StrOutputParser):
    def parse(self, text: str) -> str:
        match = re.search(r"```sql\n(.*?)\n```", text, re.DOTALL)
        return match.group(1) if match else text.strip()

import pandas as pd
import pymysql

class RagModel:
    def __init__(self,db,engine):
        self.model = ChatOllama(model=os.getenv("SQL_MODEL"), temperature=0,streaming=True)
        #self.prompt = hub.pull("rlm/text-to-sql")
        self.db=db
        self.model_chain_query=self.get_chain_extract_query()
        self.model_full_response=self.get_chain_full_response()
        self.engine=engine
        
    def get_sql_query_extractor_prompt(self):
        template="""
        Based on the table schema below, write ONLY the SQL Query that would answer the user's question.
        Do NOT include explanations or additional text. Only return the SQL query.
        {schema}
        Question: {question}
        If the question is not in the table schema, return "Esa informacion no existe"
        SQL Query:
        """
        return ChatPromptTemplate.from_template(template)
    def get_schema(self,_):
        return self.db.get_table_info()

    def get_chain_extract_query(self):
        return(    
            RunnablePassthrough.assign(schema=self.get_schema)
            | self.get_sql_query_extractor_prompt()
            | self.model
            | SQLQueryParser()
        )

    def get_prompt_full_response(self):
        template="""
                Based on the table schema below, question,sql query,and sql response,write a natural language response:
                {schema}
                Question: {question}
                SQL Query: {query}
                SQL Response: {response}
                Return a response with natural language. 
                Only return the information that is relevant to the user's question. without add any explaination. 
                Use markdown format to respond without markdwon header in your output. 
                """
        return ChatPromptTemplate.from_template(template)
    def run_query(self,query):
        return self.db.run(query,include_columns=True)
    def get_chain_full_response(self):
        
        return (
            RunnablePassthrough.assign(query=lambda x: self.get_chain_extract_query().invoke(x)).assign(schema=self.get_schema,
                                                            response=lambda x:self.run_query(x["query"])
                                                            )

        | self.get_prompt_full_response()
        | self.model
        | StrOutputParser()
        )
    async def query(self,query,websocket):
        import logging
        logging.basicConfig(level=logging.INFO)
        try:
            logging.info(query)
            async for result in self.model_full_response.astream({"question":query}):
                logging.info(result)
                await websocket.send_json({"response":result})

            otro = self.get_chain_extract_query().invoke({"question":query})
            logging.info(f"query {otro}")
            

            with self.engine.connect() as connection:
                logging.info(f"connection  {connection}")
                
                print(pd.read_sql(otro,connection).to_json())
                table=pd.read_sql(otro,connection).to_json()
                logging.info(f"Table result: {table}")
                await websocket.send_json({"table":table})
        except Exception as e:
            logging.info(f"Exception for: {e}")
            result = self.model.invoke([("system","""You are a chatbot who give apologize because the question of human input hasn't been found in database which these question were asked.
                                       Return a message explaining to user that him question was not found in database.
                                       Don't comment anything else.
                                       Return your message in markdown format."""),("human",query)])
            logging.info(result)
            await websocket.send_json({"response":result.content})
            await websocket.send_json({"table":{"error":""}})
            await websocket.send_json({"end":"__END__"})
