import os
import uuid
import re
from fastapi import HTTPException, status

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

def get_file_extension(filename: str) -> str:
    """Extracts extension and converts to lowercase."""
    _, ext = os.path.splitext(filename)
    return ext.lower()

def validate_file_extension(filename: str) -> str:
    """Validates if the file type is allowed."""
    ext = get_file_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{ext}'. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return ext.replace('.', '') # returns 'pdf', 'docx' or 'txt'

def make_unique_filename(filename: str) -> str:
    """Generates a secure, unique filename using UUID to prevent overwriting."""
    # Clean the filename from risky characters
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    unique_id = uuid.uuid4().hex
    return f"{unique_id}_{filename}"