from http.client import HTTPException
from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
import os
from langchain.schema import Document
import io
from pdf_tools import pdf_text_extraction



async def load_document(file: UploadFile):
    extension = file.filename.split(".")[-1]

    match extension:
        case "txt":
            contenido = await file.read()
            documents= contenido.decode("utf-8")  # Leer como texto

        case "pdf":

            documents =await pdf_text_extraction(file)

        case "docx":
            from docx import Document as Doc

            try:
                print("Leyendo archivo DOCX...")  # Depuración
                contenido_docx = await file.read()  # Leer contenido
                file_stream = io.BytesIO(contenido_docx)  # Convertir a stream de bytes
                doc = Doc(file_stream)  # Cargar documento en python-docx
                print("Documento cargado correctamente.")  # Depuración
                return " ".join([p.text for p in doc.paragraphs])
            except Exception as e:
                print(f"Error al procesar DOCX: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error al procesar DOCX: {str(e)}")

    return documents

# Función para dividir el texto de los documentos
async def text_split(documents, chunk_size=1000, chunk_overlap=20):
# Supongamos que 'result' es el string que obtuviste previamente
    foc=documents
    # Crear una lista con un solo documento, ya que split_documents espera un iterable
    document = Document(page_content=documents, metadata={'source': 'pdf'})
    print("document: ",document)
    print("Document to split text",type(foc))

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents([document])
    return all_splits
# Función para inicializar el modelo y tokenizer de embeddings
def init_embedding_model():
    embedding_func = OllamaEmbeddings(model="mxbai-embed-large")
    return embedding_func
