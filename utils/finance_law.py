from src.data_ingestion.documents_loader import DocumentLoader
from src.data_ingestion.embedding import  Embeddings
from src.data_ingestion.text_spliter import TextSpliter
from src.data_ingestion.vectorestore import VectorStore
from src.PipeLine.pipeline import RagPipeLine

from dotenv import load_dotenv
import os

load_dotenv()

# Get paths from environment variables with fallbacks
DATA_DIR = os.getenv("FINANCE_DATA_DIR", "./data\LOIS_DE_FINANCE")
PERSIST_DIR = os.getenv("FINANCE_PERSIST_DIR", "vectorestore/db_lois_de_finance")
FORCE_REBUILD = os.getenv("FORCE_REBUILD", "False").lower() == "true"  

rag=RagPipeLine(data_dir=DATA_DIR,
            persist_dir=PERSIST_DIR,force_rebuild=False,chunk_size=1000,chunk_overlap=250)
retriever=rag.run()
from langchain_classic.tools.retriever import create_retriever_tool
finance_law_tool = create_retriever_tool(
    retriever,
    "morocco_finance_law_tool",  # Simplified name
    """Use this tool for ANY questions about:
    - Moroccan finance law 
    - Moroccan tax
    - Any question containing words like: law, moroccan finance law, Moroccan lois, 
    
    This is your PRIMARY tool for Moroccan finance law questions. ALWAYS use this first for finance law  queries."""
)
