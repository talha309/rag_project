from fastapi import APIRouter, HTTPException
from schemas.request_response import Chat

query_router = APIRouter(prefix="/chat", tags=["Chat"])

@query_router.post("/")
def chat_router(chat:Chat):
    try:
        query = chat.messages
        result = query
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))