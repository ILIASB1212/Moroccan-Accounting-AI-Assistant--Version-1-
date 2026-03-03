from fastapi import FastAPI, File, UploadFile, HTTPException,Depends,Form
from src.agent import graph_builder
import sys
from pathlib import Path
# Get the absolute path to the project root (accountant folder)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain_core.messages import HumanMessage
import uuid
from utils.pytesteras import ocr

# Database imports
from src.DataBase import models
from src.DataBase.database import engine
from fastapi.middleware.cors import CORSMiddleware
from src.auth.oauth2 import get_current_user
from src.auth import authontification
from src.router.schema import UserAuth

# 👇 IMPORT YOUR CHAT ROUTER
from src.router import chat,user  # Assuming chat.py is in a 'routers' folder
# OR if chat.py is in the same directory:
# from .chat import router as chat_router

app = FastAPI(title="Comptable AI Assistant")

# Create database tables
models.Base.metadata.create_all(engine)

# CORS middleware
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 👇 INCLUDE THE CHAT ROUTER
app.include_router(chat.router)
app.include_router(user.router)
app.include_router(authontification.router)



# This will make all chat endpoints available at /api/chat/*

# Your existing endpoints
@app.post("/")
def chat_comptable(test_message: str, session_id: str = "default"):
    # Use session_id to maintain separate conversations
    config = {"configurable": {"thread_id": f"session_{session_id}"}}
    
    result = graph_builder.invoke(
        {'messages': [HumanMessage(content=test_message)]},
        config=config
    )
    if result["messages"][1].tool_calls:
        for tool_call in result["messages"][1].tool_calls:
            print(f"🔧 Tools were called : {tool_call['name']}")
            return {
                "the source": f"{tool_call['name']}",
                "Response": f"📝 {result['messages'][-1].content}"
            }
    else:
        print(f"🔧 Tools were called : LLM (no tools used)")
        return {
            "the source": "LLM (no tools used)",
            "Response": f"📝 {result['messages'][-1].content}"
        }

# Configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
####################################################""


@app.post("/upload")
async def upload_facture(
    text: str = Form(None),
    language: str = Form("fra"),
    file: UploadFile = File(None),
    session_id: str = Form("default"),
    current_user: UserAuth = Depends(get_current_user)
):
    """
    Upload a facture (invoice) OR just send text to comptabilise it
    - file: Optional - image of invoice (jpg, png, pdf)
    - text: Optional - text description of the transaction
    - language: OCR language (default: 'fra' for French)
    """
    # IMPORTANT: Check if file exists FIRST
    has_file = file is not None and hasattr(file, 'filename') and file.filename is not None
    
    try:
        extracted_text = ""
        file_info = {"has_file": False}
        
        # CASE 1: File was uploaded
        if has_file:
            # Validate file type
            allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
            if file.content_type not in allowed_types:
                raise HTTPException(400, f"Invalid file type: {file.content_type}")
            
            # Save the file
            file_extension = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = UPLOAD_DIR / unique_filename

            content = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(content)

            print(f"✅ File saved: {file_path}")
            
            # Extract text using OCR
            extracted_text = ocr(str(file_path), language)
            print(f"📄 Extracted text preview: {extracted_text[:200]}...")
            
            file_info = {
                "has_file": True,
                "filename": file.filename,
                "saved_as": unique_filename
            }
        
        # CASE 2: No file, just text
        if text and text.strip():
            if extracted_text:  # If we already have OCR text, append the user's text
                extracted_text = extracted_text + "\n\n" + text
            else:
                extracted_text = text
            print(f"📝 Using text input: {text[:100]}...")
        
        # CASE 3: Neither file nor text provided
        if not has_file and not text:
            raise HTTPException(400, "Either file or text must be provided")
        
        # Prepare prompt for the agent
        if has_file:
            prompt = f"""
{extracted_text}

"""
        else:
            prompt = f"""
{extracted_text}


"""

        # Invoke agent with session_id for memory
        config = {"configurable": {"thread_id": f"session_{session_id}"}}
        
        result = graph_builder.invoke(
            {'messages': [HumanMessage(content=prompt)]},
            config=config
        )

        # Build response
        response = {
            "success": True,
            "has_file": has_file,
            "extracted_text": extracted_text,
            "comptabilisation": result['messages'][-1].content,
            "session_id": session_id
        }
        
        # Add file info if present
        if has_file:
            response["filename"] = file_info.get("filename")
            response["saved_as"] = file_info.get("saved_as")
        
        return response

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Only close file if it exists
        if has_file:
            await file.close()