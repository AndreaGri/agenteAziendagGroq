import os
from agents.parser import DocumentParserAgent
from database_manager import db_manager
from dotenv import load_dotenv

load_dotenv()

def bulk_ingest():
    data_dir = "data"
    parser = DocumentParserAgent()
    
    files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
    print(f"[*] Trovati {len(files)} file. Inizio ingestione...")

    for i, file_name in enumerate(files):
        path = os.path.join(data_dir, file_name)
        print(f"[{i+1}/{len(files)}] Analizzando {file_name}...")
        try:
            data = parser.run(path)
            # Per ora usiamo 'System' come owner_id visto che non abbiamo ancora il login
            db_manager.add_profile(data, "System")
            print(f"  [OK] Salvato profilo di: {data.get('name')}")
        except Exception as e:
            print(f"  [ERRORE] Su {file_name}: {e}")

if __name__ == "__main__":
    bulk_ingest()
