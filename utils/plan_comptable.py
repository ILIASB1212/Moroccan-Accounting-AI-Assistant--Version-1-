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
            persist_dir=PERSIST_DIR,force_rebuild=False,chunk_size=500,chunk_overlap=50)
retriever=rag.run()

### Retriever To Retriever Tools
from langchain_classic.tools.retriever import create_retriever_tool
plan_comptable_tool = create_retriever_tool(
    retriever,
    "plan_comptable_general_marocain",
    """Use this tool to retrieve SPECIFIC ACCOUNT NUMBERS and their exact labels from the **Plan Comptable Général Marocain (PCGM)** — the official Moroccan chart of accounts.

    This tool is DIFFERENT from the CGNC tool — while CGNC explains accounting PRINCIPLES and RULES,
    this tool gives you the EXACT ACCOUNT CODES (numéros de comptes) needed to record any transaction.

    ALWAYS trigger this tool when you need to:

    **Look Up Specific Account Numbers**
    - Find the exact 4-digit (or more) account number for any transaction
    - Identify the correct account label (intitulé du compte)
    - Confirm which class (1–7) an account belongs to
    - Distinguish between similar accounts (e.g. 3421 Clients vs 3424 Clients douteux)

    **Record Accounting Entries (Écritures Comptables)**
    - Comptabiliser une facture d'achat ou de vente
    - Comptabiliser la TVA collectée (4455) et TVA récupérable (3455)
    - Comptabiliser un règlement client ou fournisseur
    - Comptabiliser un salaire, une charge sociale, une retenue
    - Comptabiliser une acquisition d'immobilisation
    - Comptabiliser un amortissement ou une provision
    - Comptabiliser une opération de trésorerie (banque, caisse, virement)

    **Account Classes Reference**
    - Classe 1 — Comptes de financement permanent (capital, réserves, dettes de financement)
    - Classe 2 — Comptes d'actif immobilisé (immobilisations corporelles, incorporelles, financières)
    - Classe 3 — Comptes d'actif circulant (stocks, clients, créances, régularisation actif)
    - Classe 4 — Comptes de passif circulant (fournisseurs, dettes fiscales, sociales, régularisation passif)
    - Classe 5 — Comptes de trésorerie (banques, caisse, CCP, crédits de trésorerie)
    - Classe 6 — Comptes de charges (achats, charges externes, impôts, charges de personnel, dotations)
    - Classe 7 — Comptes de produits (ventes, produits financiers, produits non courants)

    **Most Frequently Used Accounts (high-priority retrieval)**
    - 5141 Banque / 5161 Caisse
    - 3421 Clients / 4411 Fournisseurs
    - 3455 TVA récupérable / 4455 TVA facturée
    - 2321 Matériel et outillage / 2340 Matériel de transport / 2350 Mobilier de bureau
    - 6111 Achats de marchandises / 7111 Ventes de marchandises
    - 6131 Locations / 6141 Primes d'assurance / 6156 Maintenance
    - 6171 Rémunérations du personnel / 6174 Charges sociales
    - 2810–2880 Amortissements des immobilisations
    - 1111 Capital social / 1151 Réserve légale / 1191 Résultat de l'exercice

    **Specific Keywords that should trigger this tool:**
    numéro de compte, code comptable, intitulé, passer une écriture, journal,
    comptabiliser, imputer, débit, crédit, plan comptable, compte 6, compte 7,
    compte fournisseur, compte client, compte TVA, compte banque, compte caisse,
    schéma comptable, écriture d'achat, écriture de vente, écriture de paie,
    écriture d'amortissement, écriture de clôture, écriture d'inventaire

    **Important routing note:**
    - Need the RULE or PRINCIPLE behind an accounting treatment → use CGNC tool first
    - Need the EXACT ACCOUNT NUMBER to record it → use THIS tool
    - Both tools can and should be used TOGETHER for complete accounting answers
    - Need the TAX RATE to apply on a transaction → use CGI tool
    - Need a NEW measure that changed account treatment this year → use Loi de Finances tool
    """
)
