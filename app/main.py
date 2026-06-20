import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings

# Dono routers ko import karein
from api.upload import upload_router
from api.query import query_router  # Aapka chat router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Day 2: Document Ingestion and Chat Route Initialization"
)

# Uploaded files ko publicly accessible banane ke liye static mount
app.mount("/files", StaticFiles(directory=settings.UPLOAD_DIR), name="files")

# 1. Upload Router include karein
app.include_router(upload_router, prefix=settings.API_V1_STR)

# 2. Query Router include karein (Iska prefix bhi hum standard v1 hi rakhenge)
app.include_router(query_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}. Visit /docs for API documentation."}


if __name__ == "__main__":
    import uvicorn
    # Application ko chalane ke liye command
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)