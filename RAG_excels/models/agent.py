from typing import Dict
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.documents import Document
from models.tools import get_tools
import os
from fastapi import  WebSocket
import logging 
logging.basicConfig(level=logging.INFO)

class Agent: # Remove singleton because each user_session has a agent specifly to file
    
    def __init__(self, file_path: str ,use_existing: bool = False):
        self.file_path = file_path
        self.use_existing = use_existing
        self.agent=self.build_agent()
        logging.info("Agent built")

    
    def get_model(self):
        return ChatOllama(model="gpt-oss:latest", temperature=0.1)


        
    def build_agent(self):
        logging.info(f"Prompt:  {self.get_prompt()}")
        self.agent = create_agent(model=self.get_model(),
                                    tools=get_tools(),
                                    system_prompt=self.get_prompt(),
                                    checkpointer=MemorySaver()
                                )
        return self.agent
    
    def get_prompt(self):
        return f"""Eres un asistente experto en gestión de Excel.
CAPACIDADES:
1. BUSCAR datos con 'buscar_en_excel'
2. EXPLORAR estructura con 'explorar_excel' 
3. EDITAR datos con 'editar_excel' (SIEMPRE pide confirmación)

FLUJOS TÍPICOS:
1. Primero explora: "explorar_excel()"
2. Busca datos relevantes: "buscar_en_excel()"
3. Para editar: "editar_excel(hoja='Ventas', celda='B5', nuevo_valor='1500', confirmacion='SI')"

⚠️ NUNCA edites sin confirmacion='SI'
⚠️ Siempre informa qué backup se creó

All answers and actions user ask are about next file {self.file_path}"""
