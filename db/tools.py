from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
import os
model=os.getenv("MODEL")
# Función para cargar un documento PDF
def load_pdf(filename):
    loader = PyPDFLoader(filename)
    documents = loader.load()
    return documents

# Función para dividir el texto de los documentos
def text_split(documents, chunk_size=2000, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(documents)
    return all_splits
# Función para inicializar el modelo y tokenizer de embeddings
def init_embedding_model():
    embedding_func = OllamaEmbeddings(model=model)
    return embedding_func
