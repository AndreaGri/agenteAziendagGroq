from agents.scout import ScoutAgent
from agents.critic import CriticAgent
from dotenv import load_dotenv

load_dotenv()

def test_full_search():
    scout = ScoutAgent()
    critic = CriticAgent()
    
    query = "Cerco un esperto di spettroscopia a Milano"
    print(f"[*] Ricerca per: '{query}'")
    
    # 1. Lo Scout trova i candidati
    scout_results = scout.run(query)
    
    # 2. Il Critic analizza il primo risultato
    if scout_results['matches']:
        best_match = scout_results['matches'][0]
        print(f"[*] Scout ha trovato: {best_match['name']}. Passo al Critic...")
        
        validation = critic.run(query, best_match)
        print(f"\n[+] GIUDIZIO DEL CRITIC:")
        print(f"Valido: {validation['is_valid']} (Voto: {validation['score']}/10)")
        print(f"Critica: {validation['critique']}")
    else:
        print("[-] Nessun match trovato dallo Scout.")

if __name__ == "__main__":
    test_full_search()
