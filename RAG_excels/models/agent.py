from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.documents import Document
from .tools import buscar_en_excel, editar_excel, explorar_excel
from .excel_loader import load_and_process_excel, load_existing_vectorstore, save_vectorstore
import os
from fastapi import  WebSocket

class ExcelAgent:
    """Clase singleton para gestionar el agente de Excel."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.vectorstore = None
            self.retriever = None
            self.embeddings = None
            self.llm = None
            self.tools = None
            self.agent = None
            self._initialized = True
    
    def initialize(self, file_path: str = "tu_archivo.xlsx", use_existing: bool = False):
        """Inicializa el agente con el archivo Excel especificado."""
        
        if use_existing:
            # Cargar vectorstore existente
            self.vectorstore, self.retriever, self.embeddings = load_existing_vectorstore()
        else:
            # Crear nuevo vectorstore
            self.vectorstore, self.retriever, self.embeddings = load_and_process_excel(file_path)
            # Guardar para reutilizar
            save_vectorstore(self.vectorstore)
        
        # Inyectar el retriever en la herramienta buscar_en_excel
        # Creamos una versión especializada de la herramienta con el retriever inyectado
        def buscar_en_excel_with_retriever(query: str) -> tuple[str, list[Document]]:
            """Busca información relevante en el archivo Excel para responder preguntas."""
            docs = self.retriever.invoke(query)
            
            # Serializar para LLM (con metadata)
            context = "\n\n".join([
                f"Hoja: {doc.metadata.get('sheet_name', 'N/A')}\n"
                f"Celda: {doc.metadata.get('cell', 'N/A')}\n"
                f"Contenido: {doc.page_content[:300]}..."
                for doc in docs
            ])
            
            return context, docs  # LLM ve 'context', app ve 'docs'
        
        # Reemplazar la herramienta original con la versión especializada
        buscar_en_excel.func = buscar_en_excel_with_retriever
        buscar_en_excel.__func__ = buscar_en_excel_with_retriever
        
        # Configurar agente
        self.llm = ChatOllama(model="gpt-oss:latest", temperature=0.1)
        self.tools = [buscar_en_excel, editar_excel, explorar_excel]
        
        system_prompt = """Eres un asistente experto en gestión de Excel.
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
        
        self.agent = create_agent(self.llm, self.tools, system_prompt)
    
    def get_agent(self):
        """Devuelve la instancia del agente."""
        if self.agent is None:
            raise Exception("El agente no ha sido inicializado. Llama a initialize() primero.")
        return self.agent
    
    async def query(self, question:str,
              collection_name:str,
              credentials:str,
              websocket:WebSocket):
        """Realiza una consulta al agente."""
        config={"configurable":{"thread_id":credentials}}

        if self.agent is None:
            raise Exception("El agente no ha sido inicializado. Llama a initialize() primero.")
        async for result in  self.agent.astream({"messages": question},config,stream_mode="values"):
            websocket.send_text(result[-1].content)
