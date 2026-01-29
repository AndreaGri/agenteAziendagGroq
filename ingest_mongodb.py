from agents.parser import DocumentParserAgent
from database_manager import db_manager
import os
from dotenv import load_dotenv

load_dotenv()

def ingest_single():
    file_path = "data/cv_stefano_mongodb.pdf"
    print(f"[*] Ingestione di: {file_path}")
    
    parser = DocumentParserAgent()
    try:
        data = parser.run(file_path)
        db_manager.add_profile(data, "System")
        print(f"[OK] Stefano De Luca (Esperto MongoDB) aggiunto al sistema.")
    except Exception as e:
        print(f"[ERRORE] Durante l'ingestione: {e}")

if __name__ == "__main__":
    ingest_single()
