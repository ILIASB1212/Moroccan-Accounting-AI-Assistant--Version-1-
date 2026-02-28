from fastapi import FastAPI,staticfiles,File,UploadFile
from src.agent import graph_builder
# Add this at the VERY TOP of agent.py (before any other imports)
import sys
from pathlib import Path
# Get the absolute path to the project root (accountant folder)
project_root = Path(__file__).parent.parent  # Goes from src/ to accountant/
sys.path.insert(0, str(project_root))
# load librarys
from langchain_core.messages import HumanMessage

from langchain_core.messages import HumanMessage

app = FastAPI(title="Comptable AI Assistant")
@app.post("/")
def chat_comptable(test_message:str):
    result = graph_builder.invoke({'messages': HumanMessage(content=test_message)})
        # chekking tool caling if and else 
    if result["messages"][1].tool_calls:
        for tool_call in result["messages"][1].tool_calls:
            print(f"🔧 Tools were called : {tool_call['name']}")
            return {"the source":f" {tool_call['name']}",
                     "Response":f"📝 {result['messages'][-1].content}"}
    
    else:
        print(f"🔧 Tools were called : LLM (no tools used)")
        return {"the source":"LLM (no tools used)}",
                     "Response":f"📝 {result['messages'][-1].content}"}
    

from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain_core.messages import HumanMessage
from src.agent import graph_builder
import pytesseract
from utils.deepseek_ocr import ocr
from pathlib import Path

# Configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def itt(img:bytes):
    return pytesseract.image_to_string(img)


@app.post("/upload")
async def upload_facture(file: UploadFile = File(...)):
    """
    Upload a facture (invoice) and comptabilise it with enhanced OCR
    """
    try:

        extracted_text=ocr(file.file)
        # Create enhanced prompt with extracted text
        prompt = f"""TASK: Comptabiliser cette facture d'achat selon les normes CGMC (Code Général de Normalisation Comptable marocain)

TEXTE EXTRAIT DE LA FACTURE (via OCR):
{extracted_text}

INFORMATIONS IDENTIFIÉES:
- Date: 28/01/2024
- Date d'échéance: 11/02/2024
- Produit: 3 unités à 189,00€ (total 567,00€) + TVA 20%
- Service: 1 unité à 800,00€ (total 800,00€) + TVA 20%
- Remise 10% sur service: -80,00€
- Total HT: 1 287,00€
- TVA totale: 257,40€
- Total TTC: 1 544,40€

INSTRUCTIONS:
1. Analyser cette facture d'achat
2. Proposer les écritures comptables selon le plan comptable marocain avec le format:
   numéro compte débiteur | numéro compte créditeur | libellé | montant

3. Pour cette facture d'achat, utiliser:
   - Compte de charge: 6131 (Achats de matières et fournitures)
   - Compte de TVA récupérable: 3455
   - Compte fournisseur: 4411

4. Présenter l'écriture comptable complète
"""
        
        # Send to agent
        result = graph_builder.invoke({
            'messages': [HumanMessage(content=prompt)]
        })
        
        return {
            "success": True,
            "filename": file.filename,
            "extracted_text": extracted_text,
            "comptabilisation": result['messages'][-1].content
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
