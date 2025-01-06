import chromadb
async def get_chroma_client(credentials=None):
    """Simple method to get the chroma client."""

    #PERSIT_DIRECTORY=os.getenv("PERSIST_DIRECTORY")
    print("Credentials:",credentials)
    PERSIST_DIRECTORY=credentials
    return chromadb.PersistentClient(path=PERSIST_DIRECTORY)