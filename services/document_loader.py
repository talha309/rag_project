import os
from pypdf import PdfReader
from docx import Document
from fastapi import HTTPException, status

class DocumentLoaderService:
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        """
        Determines the file type and extracts raw text.
        """
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="File not found on disk."
            )

        try:
            if file_type == "txt":
                return DocumentLoaderService._extract_txt(file_path)
            elif file_type == "pdf":
                return DocumentLoaderService._extract_pdf(file_path)
            elif file_type == "docx":
                return DocumentLoaderService._extract_docx(file_path)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Unsupported file type during extraction."
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to extract text from {file_type} file: {str(e)}"
            )

    @staticmethod
    def _extract_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()

    @staticmethod
    def _extract_docx(file_path: str) -> str:
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text.append(paragraph.text)
        return "\n".join(text).strip()