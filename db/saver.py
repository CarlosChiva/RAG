import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.document_loaders import PyPDFLoader

embedding_func = OllamaEmbeddings()

def __load_pdf(filename):
    loader = PyPDFLoader(filename)
    documents = loader.load()
    return documents
def __text_split(documents):
   text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
   all_splits = text_splitter.split_documents(documents)
   return all_splits
async def create_new_collection(collection_name, document):
    documents = __load_pdf(document)
    splits=__text_split(documents)
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embedding_func,
        persist_directory=f"db1/{collection_name}",
        collection_name=collection_name
    )
    vectorstore.persist()
    print(f"Nueva colección '{collection_name}' creada con éxito.")
    return {"message": f"Nueva colección '{collection_name}' creada con éxito."}

def add_documents_to_collection(collection_name, document):
    documents = __load_pdf(document)
    splits=__text_split(documents)
    vectorstore = Chroma(
        persist_directory=f"db1/{collection_name}",
        embedding_function=embedding_func,
        collection_name=collection_name
    )
    vectorstore.add_documents(documents=splits)
    vectorstore.persist()
    print(f"Documentos añadidos a la colección '{collection_name}' con éxito.")
    return {"message": f"Documento'{document}' añadido a la colección '{collection_name}' con éxito."}

def __get_collections():
    base_directory = "db1"
    if not os.path.exists(base_directory):
        return []
    
    collections = [name for name in os.listdir(base_directory) 
                   if os.path.isdir(os.path.join(base_directory, name))]
    return collections

def show_collections():
    array_collect=[]
    collections = __get_collections()
    if collections:
        print("Colecciones existentes:")
        array_collections=[collection for collection in collections]
        return array_collections
    else:
        return []

def search_name_collection(name):
    base_directory = "db1"
    if not os.path.exists(base_directory):
        return name in os.listdir(base_directory)