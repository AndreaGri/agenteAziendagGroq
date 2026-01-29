import os
from agents.parser import DocumentParserAgent
from dotenv import load_dotenv

load_dotenv()

def test():
    # Verifica se esiste un file di test, altrimenti avvisa
    test_file = "data/test_cv.pdf"
    if not os.path.exists(test_file):
        print(f"[-] Errore: Inserisci un file PDF in {test_file} per testare l'agente.")
        return

    print(f"[*] Testando DocumentParserAgent su: {test_file}...")
    agent = DocumentParserAgent()
    try:
        result = agent.parse(test_file)
        print("[+] Estrazione completata con successo:")
        print(result)
    except Exception as e:
        print(f"[-] Errore durante il parsing: {e}")

if __name__ == "__main__":
    test()
