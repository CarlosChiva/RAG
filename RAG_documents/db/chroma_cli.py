from dotenv import load_dotenv
load_dotenv()
import os
import chromadb
async def get_chroma_client(credentials=None):
    """Simple method to get the chroma client."""

    PERSIT_DIRECTORY=os.getenv("PERSIST_DIRECTORY")
    print("Credentials:",credentials)
    PERSIST_DIRECTORY=PERSIT_DIRECTORY+"/"+credentials
    return chromadb.PersistentClient(path=PERSIST_DIRECTORY)