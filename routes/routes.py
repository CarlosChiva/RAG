from fastapi import *
from controllers import controllers

router = APIRouter()

@router.get("/")
async def index():
    result = await controllers.index()

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["error"])
    
    return result