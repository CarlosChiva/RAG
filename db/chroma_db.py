import chromadb
from db.tools import load_pdf, text_split, init_embedding_model
from langchain_community.vectorstores import Chroma



async def get_collections():
    chroma_client= chromadb.PersistentClient(path="./db")
    collections = chroma_client.list_collections()
    collection_names = [collection.name for collection in collections]
    return collection_names
# Función principal para añadir el PDF a una colección específica
async def add_pdf_to_collection(collection_name, filename=None):
    chroma_client= chromadb.PersistentClient(path="./db")

        # Crear o obtener la colección
    if chroma_client.get_collection(name=collection_name) is None:
        collection = chroma_client.create_collection(name=collection_name)

    collection= chroma_client.get_collection(name=collection_name)
        
    documents = load_pdf(filename)
    splits = text_split(documents)
    embedding_func = init_embedding_model()

        # Añadir documentos a la colección
    for i, split in enumerate(splits):
        text = split.page_content
        metadata = split.metadata
        embedding = embedding_func.embed_query(text)
        collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[f"{collection_name}_{i}"],
            embeddings=[embedding]
        )
        
    print(f"Added {len(splits)} documents to collection '{collection_name}'")
    return {"message": f"Added documents to collection '{collection_name}'"}

async def get_chroma_client():

        return chromadb.PersistentClient(path="./db")
async def get_vectorstore(collection_name):
    cli=await get_chroma_client()
            # Inicializar el almacén de vectores para la colección específica
    embedding_func = init_embedding_model()
    vectorstore = Chroma(
        client= cli,
        collection_name=collection_name,
        embedding_function=embedding_func
    )
    return vectorstore