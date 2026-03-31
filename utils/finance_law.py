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
            persist_dir=PERSIST_DIR,force_rebuild=False,chunk_size=800,chunk_overlap=200)
retriever=rag.run()
from langchain_classic.tools.retriever import create_retriever_tool
finance_law_tool = create_retriever_tool(
    retriever,
    "loi_de_finances_maroc",
    """Use this tool to answer any question related to the **Loi de Finances (LF)** — the annual Moroccan budget law voted by parliament that sets fiscal, economic, and budgetary measures for each year.

    This document is DIFFERENT from the CGI (permanent tax code) — it contains ANNUAL amendments,
    new measures, and temporary provisions that modify or complement the CGI and CGNC for a specific fiscal year.

    Trigger this tool for questions about:

    **Annual Tax Amendments & New Measures**
    - Changes to IS (Impôt sur les Sociétés) rates or rules for the year
    - Changes to IR (Impôt sur le Revenu) brackets, deductions, or thresholds
    - TVA rate changes, new exemptions, or newly taxable operations
    - New withholding tax (retenue à la source) rules introduced that year
    - New tax incentives, exonérations, or abattements introduced in the LF

    **Budget & Public Finance**
    - Budget général de l'État — recettes, dépenses, solde budgétaire
    - Plafonds des charges et des ressources de l'État
    - Dépenses d'investissement public (budget d'investissement)
    - Déficit budgétaire prévisionnel and financement du déficit
    - Recettes fiscales et non fiscales prévues

    **Economic & Social Measures**
    - Mesures de soutien aux entreprises (PME, auto-entrepreneurs)
    - Mesures sociales : retraites, CNSS, AMO contributions
    - Sectoral incentives : immobilier, agriculture, export, tourisme
    - Contribution sociale de solidarité (CSS) updates

    **Customs & Duties**
    - Droits de douane modifications
    - Tarif intérieur de consommation (TIC) changes
    - Nouvelles taxes parafiscales

    **Specific Keywords that should trigger this tool:**
    loi de finances, LF, loi de finances rectificative, LFR, budget de l'État,
    mesures fiscales, dispositions fiscales, article de la loi de finances,
    année fiscale, exercice budgétaire, recettes budgétaires, dépenses publiques,
    plafond, amendement fiscal, nouveau taux, nouvelle mesure, réforme fiscale,
    note circulaire, DGI, Trésorerie Générale du Royaume, TGR

    **Important routing note:**
    - If the question is about a PERMANENT tax rule with no mention of a specific year → use CGI tool
    - If the question mentions a specific year, recent change, new measure, or annual update → use THIS tool
    - If the question is about accounting treatment or financial statements → use CGNC tool

    Use this tool whenever the user asks about the annual budget law, yearly fiscal amendments,
    new government tax measures, or any provision introduced by a specific Loi de Finances du Maroc.
    """
)
