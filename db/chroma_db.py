import chromadb
from tools import load_pdf, text_split, init_embedding_model
from langchain_community.vectorstores import Chroma

class Chroma_custom:
    def __init__(self):
        # Inicializar el cliente de Chroma
        self.chroma_client= chromadb.PersistentClient(path="./db")


    def get_collections(self):
        collections = self.chroma_client.list_collections()
        collection_names = [collection.name for collection in collections]
        return collection_names
# Función principal para añadir el PDF a una colección específica
    def add_pdf_to_collection(self,collection_name, filename):
        documents = load_pdf(filename)
        splits = text_split(documents)
        embedding_func = init_embedding_model()
        
        # Crear o obtener la colección
        collection = self.chroma_client.get_or_create_collection(name=collection_name)
        
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
    def get_chroma_client(self):
        return self.chroma_client
    def get_vectorstore(self,collection_name):
            # Inicializar el almacén de vectores para la colección específica
        embedding_func = init_embedding_model()
        vectorstore = Chroma(
        client=self.chroma_client,
        collection_name=collection_name,
        embedding_function=embedding_func
        )
        return vectorstore