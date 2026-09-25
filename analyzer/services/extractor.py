import os
import pypdf as PyPDF2

import docx
from PIL import Image
import pytesseract

class ResumeExtractor:
    """Base Class demonstrating Object Oriented Programming (OOP) hierarchy."""
    
    def extract_text(self, file_path: str) -> str:
        """Polymorphic method to be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement extract_text()")


class PDFExtractor(ResumeExtractor):
    """Subclass for extracting text from PDF files using PyPDF2."""
    
    def extract_text(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print(f"[PDFExtractor Error]: {e}")
        return text.strip()


class DOCXExtractor(ResumeExtractor):
    """Subclass for extracting text from DOCX files using python-docx."""
    
    def extract_text(self, file_path: str) -> str:
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                if paragraph.text:
                    text += paragraph.text + "\n"
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text:
                            text += cell.text + " "
                    text += "\n"
        except Exception as e:
            print(f"[DOCXExtractor Error]: {e}")
        return text.strip()


class ImageExtractor(ResumeExtractor):
    """Subclass for extracting text from Images (JPG, JPEG, PNG) using Pillow and pytesseract."""
    
    def extract_text(self, file_path: str) -> str:
        text = ""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
        except Exception as e:
            print(f"[ImageExtractor Error / Tesseract notice]: {e}")
        return text.strip()


def get_extractor(file_path: str) -> ResumeExtractor:
    """Factory function returning the appropriate extractor based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return PDFExtractor()
    elif ext in ['.docx', '.doc']:
        return DOCXExtractor()
    elif ext in ['.jpg', '.jpeg', '.png']:
        return ImageExtractor()
    else:
        raise ValueError(f"Unsupported file format: {ext}")
