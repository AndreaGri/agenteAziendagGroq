from agents.parser import DocumentParserAgent
from database_manager import db_manager
import os
from dotenv import load_dotenv

load_dotenv()

def run_test():
    test_file = "data/test_cv.pdf"
    if not os.path.exists(test_file):
        print(f"[-] Errore: manca il PDF in {test_file}. Crea prima il PDF!")
        return

    print("[1] Avvio Agente Parser...")
    parser = DocumentParserAgent()
    try:
        extracted_data = parser.run(test_file)
        print(f"[+] Dati estratti correttamente per: {extracted_data.get('name')}")

        print("[2] Salvataggio nel Vector DB...")
        db_manager.add_profile(extracted_data)
        print("[+] Salvataggio completato!")
        
    except Exception as e:
        print(f"[-] Errore durante l'ingestione: {e}")

if __name__ == "__main__":
    run_test()
