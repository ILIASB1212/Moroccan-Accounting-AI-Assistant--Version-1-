import streamlit as st
from dotenv import load_dotenv
import io

load_dotenv()

# Try importing PDF and DOCX libraries
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    st.warning("PyPDF2 not installed. PDF support disabled. Run: pip install PyPDF2")

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    st.warning("python-docx not installed. Word document support disabled. Run: pip install python-docx")

def read_file_content(uploaded_file):
    """
    Read content from uploaded file based on its type
    """
    file_content = ""
    
    # Get file type
    file_type = uploaded_file.type
    
    try:
        if file_type == "text/plain":
            # Handle TXT files
            file_content = uploaded_file.getvalue().decode("utf-8")
            
        elif file_type == "application/pdf":
            # Handle PDF files
            if not PDF_AVAILABLE:
                st.error("PDF support not available. Please install PyPDF2: pip install PyPDF2")
                return ""
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            for page_num, page in enumerate(pdf_reader.pages, 1):
                extracted_text = page.extract_text()
                if extracted_text:
                    file_content += f"--- Page {page_num} ---\n{extracted_text}\n\n"
                    
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Handle DOCX files
            if not DOCX_AVAILABLE:
                st.error("Word document support not available. Please install python-docx: pip install python-docx")
                return ""
            
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    file_content += paragraph.text + "\n"
                    
        else:
            st.warning(f"Unsupported file type: {file_type}")
            return ""
            
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return ""
    
    return file_content