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
            persist_dir=PERSIST_DIR,force_rebuild=False,chunk_size=1000,chunk_overlap=200)
retriever=rag.run()
### Retriever To Retriever Tools
from langchain_classic.tools.retriever import create_retriever_tool

cgnc_tool = create_retriever_tool(
    retriever,
    "code_general_normalisation_comptable_maroc",
    """Use this tool to answer any question related to Moroccan accounting standards as defined in the **Code Général de Normalisation Comptable (CGNC)** — the official Moroccan accounting normalization framework.

    Trigger this tool for questions about:

    **Plan Comptable Général Marocain (PCGM)**
    - Chart of accounts structure (classes 1 to 7)
    - Account numbering, naming, and classification
    - Comptes de financement permanent (classe 1)
    - Comptes d'actif immobilisé (classe 2)
    - Comptes d'actif circulant (classe 3)
    - Comptes de passif circulant (classe 4)
    - Comptes de trésorerie (classe 5)
    - Comptes de charges (classe 6)
    - Comptes de produits (classe 7)

    **Financial Statements (États de Synthèse)**
    - Bilan comptable (balance sheet) — structure, presentation rules
    - Compte de Produits et Charges (CPC) — income statement format
    - État des Soldes de Gestion (ESG) — management performance ratios
    - Tableau de Financement (TF) — cash flow and financing statement
    - État des Informations Complémentaires (ETIC) — notes to financial statements

    **Accounting Principles & Concepts**
    - Principes comptables fondamentaux (continuité, prudence, permanence des méthodes)
    - Comptabilité d'engagement vs trésorerie
    - Coût historique and valeur nette comptable
    - Régularisations (charges/produits constatés d'avance, charges à payer)

    **Asset Accounting**
    - Immobilisations corporelles, incorporelles, financières
    - Amortissement (méthodes linéaire, dégressif)
    - Provisions pour dépréciation
    - Cessions d'immobilisations and plus/moins-values

    **Operations & Transactions**
    - Stocks : méthodes d'évaluation (CMUP, FIFO), provisionnement
    - Créances et dettes : lettrage, provisionnement des créances douteuses
    - Effets de commerce : escompte, endossement, impayés
    - Opérations en devises et écarts de conversion

    **Specific Keywords that should trigger this tool:**
    CGNC, plan comptable, bilan, CPC, ESG, ETIC, tableau de financement,
    immobilisation, amortissement, provision, charge, produit, résultat,
    compte, écriture comptable, journal, grand livre, balance, clôture,
    régularisation, stock, créance, dette, trésorerie, capitaux propres,
    financement permanent, actif immobilisé, actif circulant, passif circulant

    Use this tool whenever the user asks about accounting entries, financial statement
    preparation, account classification, or any article or principle from the CGNC marocain.
    """
)
