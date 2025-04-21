#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel
#from config import Config


router = APIRouter()    
@router.get("/query")
async def query(query:str,credentials  = Depends(credentials_controllers.verify_jws)
                        ):
    # linkear credenciales para id conversacion y id usuario
    # modelos de ollama disponibles
    result = await controllers.query(query,credentials)
    return {"result":result}


@router.get("/get_ollama_models")
async def query(credentials  = Depends(credentials_controllers.verify_jws)
                        ):
    # linkear credenciales para id conversacion y id usuario
    # modelos de ollama disponibles
    result = await controllers.get_ollama_models()
    return {"result":result}