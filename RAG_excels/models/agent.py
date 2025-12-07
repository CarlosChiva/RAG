from typing import Dict
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.documents import Document
from .tools import buscar_en_excel, editar_excel, explorar_excel
from ..services.excel_loader import load_and_process_excel, load_existing_vectorstore, save_vectorstore
import os
from fastapi import  WebSocket


class Agent: # Remove singleton because each user_session has a agent specifly to file
    
    def __init__(self, file_path: str , use_existing: bool = False):
        self.initialize(file_path, use_existing)
        self.agent=self.build_agent()
        return self.agent        
    
    def get_model(self):
        return ChatOllama(model="gpt-oss:latest", temperature=0.1)

    def get_tools(self):
# Inyectar el retriever en la herramienta buscar_en_excel
        # Creamos una versión especializada de la herramienta con el retriever inyectado

        # Reemplazar la herramienta original con la versión especializada
        # Configurar agente
        self.tools = [buscar_en_excel, editar_excel, explorar_excel]
        
    def build_agent(self):
                self.agent = create_agent(self.get_model(),
                                            self.get_tools(),
                                            self.get_prompt(),
                                            checkpointer=MemorySaver()
                                        )
    def get_prompt(self):
        return"""Eres un asistente experto en gestión de Excel.
CAPACIDADES:
1. BUSCAR datos con 'buscar_en_excel'
2. EXPLORAR estructura con 'explorar_excel' 
3. EDITAR datos con 'editar_excel' (SIEMPRE pide confirmación)

FLUJOS TÍPICOS:
1. Primero explora: "explorar_excel()"
2. Busca datos relevantes: "buscar_en_excel()"
3. Para editar: "editar_excel(hoja='Ventas', celda='B5', nuevo_valor='1500', confirmacion='SI')"

⚠️ NUNCA edites sin confirmacion='SI'
⚠️ Siempre informa qué backup se creó"""
        
        



    


