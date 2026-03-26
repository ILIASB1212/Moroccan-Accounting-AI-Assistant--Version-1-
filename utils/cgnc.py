from src.data_ingestion.documents_loader import DocumentLoader
from src.data_ingestion.embedding import  Embeddings
from src.data_ingestion.text_spliter import TextSpliter
from src.data_ingestion.vectorestore import VectorStore
from pathlib import Path
from src.PipeLine.pipeline import RagPipeLine
from dotenv import load_dotenv
import os

load_dotenv()

# Get paths from environment variables with fallbacks
DATA_DIR = os.getenv("CGNC_DATA_DIR", "./data/CGNC")
PERSIST_DIR = os.getenv("CGNC_PERSIST_DIR", "vectorestore/db_CGNC")
FORCE_REBUILD = os.getenv("FORCE_REBUILD", "False").lower() == "true"  

rag=RagPipeLine(data_dir=DATA_DIR,
            persist_dir=PERSIST_DIR,force_rebuild=False,chunk_size=800,chunk_overlap=200)
retriever=rag.run()
### Retriever To Retriever Tools
from langchain_classic.tools.retriever import create_retriever_tool

cgnc_tool = create_retriever_tool(
    retriever,
    "cgnc_accounting_tool",
    """Use this tool for ANY questions about:
    - Moroccan accounting (CGNC - Code Général de Normalisation Comptable)
    - Financial reporting standards in Morocco
    - Moroccan tax accounting rules
    - Chart of accounts (Plan comptable marocain)
    - Accounting treatments specific to Morocco
    - Any question containing words like: CGNC, comptabilité marocaine, Moroccan accounting, Plan comptable
    
    This is your PRIMARY tool for Moroccan accounting questions. ALWAYS use this first for accounting queries."""
)
