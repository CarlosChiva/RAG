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
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
from langchain_core.runnables import RunnablePassthrough

class DataBase:
    def __init__(self,conf:Config):
        self.driver=self.extract_driver(conf.type_db)
        self.user=conf.user
        self.password=conf.password
        self.host=conf.host
        self.port=conf.port
        self.database_name=conf.database_name
        self.connect_db()

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



class SQLQueryParser(StrOutputParser):
    def parse(self, text: str) -> str:
        match = re.search(r"```sql\n(.*?)\n```", text, re.DOTALL)
        return match.group(1) if match else text.strip()


class RagModel:
    def __init__(self,db):
        self.model = ChatOllama(model=os.getenv("SQL_MODEL"), temperature=0)
        #self.prompt = hub.pull("rlm/text-to-sql")
        self.db=db
        self.model_chain_query=self.get_chain_extract_query()
        self.model_full_response=self.get_chain_full_response()
        
    def get_sql_query_extractor_prompt(self):
        template="""
        Based on the table schema below, write ONLY the SQL Query that would answer the user's question.
        Do NOT include explanations or additional text. Only return the SQL query.
        {schema}
        Question: {question}
        SQL Query:
        """
        return ChatPromptTemplate.from_template(template)
    def get_schema(self,_):
        return self.db.get_table_info()

    def get_chain_extract_query(self):
        return(    RunnablePassthrough.assign(schema=self.get_schema)
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
                Return a response with natural language. only return the information that is relevant to the user's question. without add any explaination 
                """
        return ChatPromptTemplate.from_template(template)
    def run_query(self,query):
        return self.db.run(query)
    def get_chain_full_response(self):
        
        return (
            RunnablePassthrough.assign(query=lambda x: self.get_chain_extract_query().invoke(x)).assign(schema=self.get_schema,
                                                            response=lambda x:self.run_query(x["query"])
                                                            )

        | self.get_prompt_full_response()
        | self.model
        | StrOutputParser()
        )
    def query(self,query):
        result=self.model_full_response.invoke({"question":query})
        otro=self.get_chain_extract_query().invoke({"question":query})
        print(self.db.run(otro))
        return result