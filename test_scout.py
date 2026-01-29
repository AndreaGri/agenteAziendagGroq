from agents.scout import ScoutAgent
from dotenv import load_dotenv
import os

load_dotenv()

def test_scout():
    # Verifica se l'API KEY è presente
    if not os.getenv("GROQ_API_KEY"):
        print("[-] Errore: GROQ_API_KEY non trovata nel file .env")
        return

    scout = ScoutAgent()
    
    # Query di test
    query = "Cerco un esperto che conosca Python e analisi dati"
    
    print(f"[*] Agente Scout in azione sulla query: '{query}'...")
    try:
        analysis = scout.run(query)
        print("\n[+] Analisi dello Scout:")
        print(f"Ragionamento: {analysis.get('reasoning', 'N/A')}")
        print("-" * 30)
        for match in analysis.get('matches', []):
            print(f"- Trovato: {match.get('name')} | Skills: {match.get('skills')}")
    except Exception as e:
        print(f"[-] Errore durante lo scouting: {e}")

if __name__ == "__main__":
    test_scout()
