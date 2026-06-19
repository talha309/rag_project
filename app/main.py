from fastapi import FastAPI
from api.query import query_router
from api.upload import upload_router
app = FastAPI()

@app.get("/")
def start():
    return{
        "Welcome to RAG-Application."
    }

app.include_router(query_router, prefix="/api", tags=["query"])
app.include_router(upload_router, prefix="/api", tags=["Upload Files"])