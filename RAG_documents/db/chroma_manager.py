import sys
sys.path.append('../app/db/')
from tools import load_document, text_split, init_embedding_model
from langchain_chroma import Chroma
import uuid

async def get_collections(cli)->list[str]:
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
        
    documents = await load_document(filename)
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


async def get_vectorstore(cli,collection_name):
    
    """ Simple method to get the vectorstore. Return vectorstore with the collection_name passed as argument."""

    embedding_func =  init_embedding_model()
    vectorstore = Chroma(
        client= cli,
        collection_name=collection_name,
        embedding_function=embedding_func
    )
    return vectorstore

async def remove_collection_db(collection_name,cli):
    """Method to remove a collection. Returns a message indicating the success of the operation."""

    cli.delete_collection(collection_name)
    return {"message": f"Removed collection '{collection_name}'"}
