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
@router.post("/question")
async def llm_response(input: str,
                        database_conf:Config,
                        credentials  = Depends(credentials_controllers.verify_jws)
                        ):
    
    result = await controllers.querier(question=input,conf=database_conf)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    
    return result


@router.get("/get-list-configurations")
async def get_collections_name(credentials  = Depends(credentials_controllers.verify_jws)):
    result = await controllers.get_configurations(credentials)
    print("Return get_list_configurations  ",result)
    return result

@router.post("/add_configuration")
async def delete_collection(conf: Config,
                            credentials  = Depends(credentials_controllers.verify_jws)):
    
    result = await controllers.add_configurations(credentials,conf)
    return result

@router.get("/try-connection")  
async def try_connection(    
    connection_name: str = Query(...),
    type_db: str = Query(...),
    user: str = Query(...),
    password: str = Query(...),
    host: str = Query(...),
    port: str = Query(...),
    database_name: str = Query(...),credentials  = Depends(credentials_controllers.verify_jws)):
    conf = Config(
        connection_name=connection_name,
        type_db=type_db,
        user=user,
        password=password,
        host=host,
        port=port,
        database_name=database_name
    )
    if await controllers.try_connection(conf):
        return True
    else:
        return False

@router.delete("/remove-configuration")
async def remove_conf(conf_rm:Config,
                                credentials  = Depends(credentials_controllers.verify_jws)):    
    result =await controllers.remove_configuration(conf_rm,credentials)    
    return {"Response":result}