import pytesseract
from PIL import Image
import os

# Set Tesseract path (for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr(image_path: str,lang:str) -> str:
    """
    Extract text from an invoice image using Tesseract OCR
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return f"Error: File not found at {image_path}"
        
        # Open image
        img = Image.open(image_path)
        
        # Configure for invoice text (tables, numbers, French)
        config = r'--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzàâäéèêëìíîïðñòóôõöùúûüýÿ€$.%/-'
        
        # Extract text in French - FIXED: pytteseract -> pytesseract
        text = pytesseract.image_to_string(img, lang=lang, config=config)
        
        return text.strip()
        
    except Exception as e:
        return f"Error: {e}"
