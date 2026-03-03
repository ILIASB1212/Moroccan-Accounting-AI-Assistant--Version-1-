from src.data_ingestion.documents_loader import DocumentLoader
from src.data_ingestion.embedding import  Embeddings
from src.data_ingestion.text_spliter import TextSpliter
from src.data_ingestion.vectorestore import VectorStore
from src.PipeLine.pipeline import RagPipeLine

from dotenv import load_dotenv
import os

load_dotenv()

# Get paths from environment variables with fallbacks
DATA_DIR = os.getenv("PLAN_COMPTABLE_DATA_DIR", "./data\PLAN_COMPTABLE")
PERSIST_DIR = os.getenv("PLAN_COMPTABLE_PERSIST_DIR", "vectorestore/db_plan_comptable")
FORCE_REBUILD = os.getenv("FORCE_REBUILD", "False").lower() == "true" 


rag=RagPipeLine(data_dir=DATA_DIR,
            persist_dir=PERSIST_DIR,force_rebuild=False,chunk_size=100,chunk_overlap=20)
retriever=rag.run()

### Retriever To Retriever Tools
from langchain_classic.tools.retriever import create_retriever_tool
plan_comptable_tool = create_retriever_tool(
    retriever,
    "plan_comptable_tool",  # Simplified name
    """Use this tool to help in accountant operations:
    - Moroccan accounting 
    - les classe de bilan 
    - can work with code general de normalisation comptable to get specefic numbers 
    - use it if you want to comptabilise une facture ou une operation
    - Chart of accounts (Plan comptable marocain)
    - Accounting treatments specific to Morocco
    
    This is your PRIMARY tool for classes comptabilisation questions. ALWAYS use this first to know the classes for comptabilisation des operation queries."""
)
