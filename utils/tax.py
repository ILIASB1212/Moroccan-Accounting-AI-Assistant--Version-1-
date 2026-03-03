from src.PipeLine.pipeline import RagPipeLine

from dotenv import load_dotenv
import os

load_dotenv()

# Get paths from environment variables with fallbacks
DATA_DIR = os.getenv("CGI_DATA_DIR", "./data\CGI")
PERSIST_DIR = os.getenv("CGI_PERSIST_DIR", "vectorestore/db_CGI")
FORCE_REBUILD = os.getenv("FORCE_REBUILD", "False").lower() == "true" 

rag=RagPipeLine(data_dir=DATA_DIR,
            persist_dir=PERSIST_DIR,force_rebuild=False,chunk_size=1000,chunk_overlap=250)

retriever=rag.run()
### Retriever To Retriever Tools
from langchain_classic.tools.retriever import create_retriever_tool
CGI_tool = create_retriever_tool(
    retriever,
    "general_code_of_tax_tool",  # Simplified name
    """Use this tool for ANY questions about:
    - Moroccan tax
    - fiscal
    - Moroccan tax rules
    - tax related to accounting
    - Any question containing words like: tax, impot,fiscal
    This is your PRIMARY tool for Moroccan accounting questions. ALWAYS use this first for accounting/tax/fiscality queries."""
)
