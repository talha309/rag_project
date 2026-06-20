from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str
    filename: str
    stored_filename: str
    file_url: str
    file_type: str
    characters: int
    extracted_text_preview: str
    
class Chat(BaseModel):
    messages: str