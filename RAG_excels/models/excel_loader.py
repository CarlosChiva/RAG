import pandas as pd
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import os

# Configuración global
EXCEL_PATH = "tu_archivo.xlsx"

def load_and_process_excel(file_path: str = EXCEL_PATH):
    """Carga y procesa un archivo Excel para crear un vector store."""
    
    # 2. Cargar y procesar Excel
    loader = UnstructuredExcelLoader(file_path)  # Ruta al Excel
    docs = loader.load()

    # Convertir a chunks con metadata de hoja/celda
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(docs)

    # 3. Crear vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    return vectorstore, retriever, embeddings

def load_existing_vectorstore(index_path: str = "excel_index"):
    """Carga un vector store existente."""
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    return vectorstore, retriever, embeddings

def save_vectorstore(vectorstore, index_path: str = "excel_index"):
    """Guarda el vector store para reutilizar."""
    vectorstore.save_local(index_path)
