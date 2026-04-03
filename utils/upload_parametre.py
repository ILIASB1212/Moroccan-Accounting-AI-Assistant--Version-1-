import streamlit as st
from dotenv import load_dotenv
import io
import os
import pytesseract
from PIL import Image

load_dotenv()

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Try importing PDF and DOCX libraries
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

def ocr_image(image_bytes: bytes, lang: str = "fra") -> str:
    """Extract text from image bytes using Tesseract OCR"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        config = r'--psm 6'
        text = pytesseract.image_to_string(img, lang=lang, config=config)
        return text.strip()
    except Exception as e:
        return f"OCR Error: {e}"

def read_file_content(uploaded_file) -> str:
    """
    Read content from uploaded file based on its type.
    Supports: TXT, PDF, DOCX, JPG, JPEG, PNG, TIFF, BMP
    """
    file_content = ""
    file_type = uploaded_file.type
    file_bytes = uploaded_file.getvalue()

    try:
        # --- TXT ---
        if file_type == "text/plain":
            file_content = file_bytes.decode("utf-8")

        # --- PDF ---
        elif file_type == "application/pdf":
            if not PDF_AVAILABLE:
                st.error("Install PyPDF2: pip install PyPDF2")
                return ""
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            for page_num, page in enumerate(pdf_reader.pages, 1):
                extracted = page.extract_text()
                if extracted:
                    file_content += f"--- Page {page_num} ---\n{extracted}\n\n"

        # --- DOCX ---
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            if not DOCX_AVAILABLE:
                st.error("Install python-docx: pip install python-docx")
                return ""
            doc = Document(io.BytesIO(file_bytes))
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    file_content += paragraph.text + "\n"

        # --- IMAGES (OCR) ---
        elif file_type in ["image/jpeg", "image/jpg", "image/png", "image/tiff", "image/bmp"]:
            with st.spinner("Extracting text from image..."):
                lang = st.selectbox(
                    "OCR Language",
                    options=["fra", "eng", "ara"],
                    format_func=lambda x: {"fra": "French", "eng": "English", "ara": "Arabic"}[x],
                    key=f"ocr_lang_{uploaded_file.name}"
                )
                file_content = ocr_image(file_bytes, lang=lang)

            if file_content:
                st.success("Text extracted from image successfully")
                with st.expander("Preview extracted text"):
                    st.text(file_content)
            else:
                st.warning("No text detected in image")

        else:
            st.warning(f"Unsupported file type: {file_type}")
            return ""

    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return ""

    return file_content