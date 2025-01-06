import chromadb
import sys
sys.path.append('../app/db/')
from tools import load_pdf, text_split, init_embedding_model
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
load_dotenv()
import uuid

async def get_collections(cli):
    """Method to get the name of collections. Returns a list of collection names."""

    collections = cli.list_collections()
    collection_names = [collection.name for collection in collections]

    return collection_names

# Función principal para añadir el PDF a una colección específica
async def add_pdf_to_collection(filename,name_collection,cli):

    """Method to add a PDF to a collection."""
    """ Collection_name and filename to pdf are required to add a pdf to a collection."""
    """Returns a message indicating the success of the operation."""

        # Crear o obtener la colección
    collections= await get_collections(cli) 

    if name_collection not in collections:
        collection = cli.create_collection(name=name_collection)
    collection= cli.get_collection(name=name_collection)
        
    documents = await load_pdf(filename)
    splits = await text_split(documents)
    embedding_func = init_embedding_model()
    
    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for split in splits:
        text = split.page_content
        metadata = split.metadata
        embedding = embedding_func.embed_query(text)
        
        ids.append(str(uuid.uuid4()))
        documents.append(text)
        metadatas.append(metadata)
        embeddings.append(embedding)
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )
    
    #print(f"Added {len(splits)} documents to collection '{collection_name}'")
    return {"message": f"Added {len(splits)} documents to collection '{name_collection}'"}


async def get_vectorstore(cli):
    
    """ Simple method to get the vectorstore. Return vectorstore with the collection_name passed as argument."""
    collection_name=os.getenv("COLLECTION_NAME")
    # cli=await get_chroma_client()
            # Inicializar el almacén de vectores para la colección específica
    embedding_func =  init_embedding_model()
    vectorstore = Chroma(
        client= cli,
        collection_name=collection_name,
        embedding_function=embedding_func
    )
    return vectorstore

async def remove_collection_db():
    """Method to remove a collection. Returns a message indicating the success of the operation."""
    collection_name=os.getenv("COLLECTION_NAME")
    cli=await get_chroma_client()
    cli.delete_collection(collection_name)
    return {"message": f"Removed collection '{collection_name}'"}

#-------------------------------------Mocks to try funcionalities -----------------
def get_chroma_client_mock():
    """Simple method to get the chroma client."""
    PERSIT_DIRECTORY=os.getenv("PERSIST_DIRECTORY")

    return chromadb.PersistentClient(path=PERSIT_DIRECTORY)
def get_vectorstore_mock(collection_name):

    cli= get_chroma_client_mock()
            # Inicializar el almacén de vectores para la colección específica
    embedding_func = init_embedding_model()
    vectorstore = Chroma(
        client= cli,
        collection_name=collection_name,
        embedding_function=embedding_func
    )
    return vectorstore

def get_collections_mock():
    PERSIT_DIRECTORY=os.getenv("PERSIST_DIRECTORY")

    chroma_client= chromadb.PersistentClient(path=PERSIT_DIRECTORY)
    collections = chroma_client.list_collections()
    collection_names = [collection.name for collection in collections]
    return collection_names

def add_pdf_to_collection_mock(collection_name, filename=None):
    PERSIT_DIRECTORY=os.getenv("PERSIST_DIRECTORY")

    chroma_client= chromadb.PersistentClient(path=PERSIT_DIRECTORY)
    collections=get_collections_mock()    # Crear o obtener la colección
    if collection_name not in collections:
        collection = chroma_client.create_collection(name=collection_name)

    collection= chroma_client.get_collection(name=collection_name)
        
    documents = load_pdf(filename)
    splits = text_split(documents)
    embedding_func = init_embedding_model()
    
    num_documents = collection.count()
    print(f"La colección '{collection_name}' tiene {num_documents} documentos.")

        # Añadir documentos a la colección
    for i, split in enumerate(splits):
        text = split.page_content
        print(text)
        metadata = split.metadata
        embedding = embedding_func.embed_query(text)
        collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[f"{uuid.uuid4()}" for _ in range(len(splits))],
            embeddings=[embedding]
        )
        

    print(f"La colección '{collection_name}' tiene {num_documents} documentos.")

    return {"message": f"Added documents to collection '{collection_name}'"}

