from src.PipeLine.pipeline import RagPipeLine

from dotenv import load_dotenv
import os

load_dotenv()

# Get paths from environment variables with fallbacks
DATA_DIR = os.getenv("CGI_DATA_DIR", "./data\CGI")
PERSIST_DIR = os.getenv("CGI_PERSIST_DIR", "vectorestore/db_CGI")
FORCE_REBUILD = os.getenv("FORCE_REBUILD", "False").lower() == "true" 

rag=RagPipeLine(data_dir=DATA_DIR,
            persist_dir=PERSIST_DIR,force_rebuild=False,chunk_size=1500,chunk_overlap=300)

retriever=rag.run()
### Retriever To Retriever Tools
from langchain_classic.tools.retriever import create_retriever_tool
CGI_tool = create_retriever_tool(
    retriever,
    "code_general_des_impots_morocco",
    """Use this tool to answer any question related to Moroccan tax law as defined in the **Code Général des Impôts (CGI)** — the official Moroccan General Tax Code.

    Trigger this tool for questions about:

    **Direct Taxes (Impôts Directs)**
    - Impôt sur le Revenu (IR) — income tax on salaries, self-employment, rental income, capital gains
    - Impôt sur les Sociétés (IS) — corporate income tax, rates, deductions, tax base calculation
    - Contribution Sociale de Solidarité (CSS)

    **Indirect Taxes (Impôts Indirects)**
    - Taxe sur la Valeur Ajoutée (TVA) — VAT rates (0%, 7%, 10%, 14%, 20%), exemptions, deductibility
    - Taxe Intérieure de Consommation (TIC)

    **Registration & Stamp Duties (Droits d'Enregistrement et de Timbre)**
    - Property transfers, lease agreements, company formation acts
    - Droits de timbre on official documents

    **Tax Obligations & Procedures**
    - Tax filing deadlines (délais de déclaration)
    - Withholding tax (retenue à la source)
    - Tax audit procedures (contrôle fiscal, vérification de comptabilité)
    - Penalties and late payment interest (majorations, pénalités)
    - Tax exemptions and incentives (exonérations, abattements)

    **Specific Keywords that should trigger this tool:**
    impôt, taxe, fiscal, IS, IR, TVA, CGI, retenue, exonération, abattement, déclaration fiscale,
    cotisation, déduction, amortissement fiscal, déficit reportable, crédit d'impôt,
    résultat fiscal, base imposable, taux d'imposition, contribution, droits d'enregistrement

    Use this tool whenever the user asks about tax rates, tax calculations, tax obligations,
    fiscal procedures, or any article from the Code Général des Impôts du Maroc.
    """
)