from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql.base import SQLDatabaseChain
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama
from langchain import hub
from dotenv import load_dotenv
import os
from enums_type import Enumms as ennum
from config import Config
load_dotenv()
from sqlalchemy import create_engine

class DataBase:
    def __init__(self,conf:Config):
        self.driver=self.extract_driver(conf.type_db)
        self.user=conf.user
        self.password=conf.password
        self.host=conf.host
        self.port=conf.port
        self.database_name=conf.database_name

    def extract_driver(self,type_db):
        print(type_db)
        print(type(type_db))
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
    def try_connect(self):
        # Construcción de la URL de conexión
        database_url = f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"
        try:
            # Crear un motor de SQLAlchemy
            engine = create_engine(database_url)
        except Exception as e:
            print(f"Error al crear el motor de SQLAlchemy: {e}")
            return {"response":"Can't create the SQLAlchemy engine."}
        # Probar la conexión
        try:
            with engine.connect() as connection:
                pass
            return True
             
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False
    def connect_db(self):
        self.database = SQLDatabase.from_uri(f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}")

class RagModel:
    def __init__(self):
        self.model = ChatOllama(model=os.getenv("SQL_MODEL"), temperature=0)
        self.prompt = hub.pull("rlm/text-to-sql")
        
    
    def get_sql_agent(self,database):
       return SQLDatabaseChain(self.model, db=database, agent_type="openai-tools",prompt=self.prompt)
    
    def query(self,query,database):
        result=self.get_sql_agent(database).run(query)
        return result