
from db import saver
async def index():
    return {"message": "Hello World"}

async def new_collection(documents):
    maker= await saver.create_new_collection(collection_name="first", pdf_path=documents)
    return maker
