from dotenv import load_dotenv
load_dotenv()
import os
import chromadb
from chromadb.api.client import Client
async def get_chroma_client(credentials=None)-> Client:
    """Simple method to get the chroma client."""
    PERSIT_DIRECTORY=os.getenv("PERSIST_DIRECTORY")
    PERSIST_DIRECTORY=PERSIT_DIRECTORY+"/"+credentials
    return chromadb.PersistentClient(path=PERSIST_DIRECTORY)