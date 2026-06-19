from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os 
import shutil # file ko move , delete and so on.
upload_router = APIRouter()
# ensure uploads folder exist
UPLOAD_DIR = "./uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
# static file step-up
upload_router.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")
# upload file api

@upload_router.post("/upload")
def upload_file(file: UploadFile= File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not filename:
        raise HTTPException(status_code=400, detail="file not selected")
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return{
            "message":"file uploaded successfully",
            "filename":filename,
            "file_url":f"localHost:8000/files/{filename}"
        }
    # get file URL api

@upload_router.get("/files/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="file not found")
    
    return{
        "file_url":f"http://127.0.01:8000/files/{filename}"
    }
