import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.config import settings
from utils.file_utils import validate_file_extension, make_unique_filename
from services.document_loader import DocumentLoaderService
from schemas.request_response import UploadResponse

upload_router = APIRouter(prefix="/files", tags=["Document Ingestion"])

@upload_router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    # 1. Validate file extension
    file_type = validate_file_extension(file.filename)
    
    # 2. Create safe & unique filename
    stored_filename = make_unique_filename(file.filename)
    file_path = os.path.join(settings.UPLOAD_DIR, stored_filename)
    
    try:
        # 3. Save file asynchronously to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )
    finally:
        await file.close() # Always close the file stream

    # 4. Extract text using DocumentLoaderService
    extracted_text = DocumentLoaderService.extract_text(file_path, file_type)
    
    # 5. Build standard response
    file_url = f"{settings.BASE_URL}/files/{stored_filename}"
    preview = extracted_text[:300] + "..." if len(extracted_text) > 300 else extracted_text

    return UploadResponse(
        message="File uploaded and text extracted successfully",
        filename=file.filename,
        stored_filename=stored_filename,
        file_url=file_url,
        file_type=file_type,
        characters=len(extracted_text),
        extracted_text_preview=preview
    )