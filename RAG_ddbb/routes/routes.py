#from tempfile import NamedTemporaryFile
from fastapi import *
from controllers import controllers
from controllers import credentials_controllers
import tempfile
import os
from pydantic import BaseModel
from config import Config

router = APIRouter()
class User(BaseModel):
    username: str
    password: str
class CollectionRequest(BaseModel):
    collection_name: str
#-------------------------Principal routes-----------------------
@router.get("/question")
async def llm_response(input: str,
                        database_conf:Config,
                        credentials  = Depends(credentials_controllers.verify_jws)
                        ):
    
    result = await controllers.querier(question=input,conf=database_conf,credentials=credentials)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    
    return result


@router.get("/get-list-configurations")
async def get_collections_name(credentials  = Depends(credentials_controllers.verify_jws)):
    result = await controllers.get_configurations(credentials)
    return result

@router.post("/add_configuration")
async def delete_collection(conf: Config,
                            credentials  = Depends(credentials_controllers.verify_jws)):
    result = await controllers.add_configurations(credentials,conf)
    return result

