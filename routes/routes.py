from fastapi import *
from controllers import controllers

router = APIRouter()

@router.get("/llm-response")
async def llm_response(input: str):
    result = await controllers.user_input(input)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    
    return result