from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from agents.scout import ScoutAgent
from agents.critic import CriticAgent
from agents.connector import KnowledgeConnectorAgent

# Definizione dello Stato del Grafo
class AgentState(TypedDict):
    query: str
    results: List[dict]
    validated_results: List[dict]
    final_output: dict

# Inizializzazione Agenti
scout = ScoutAgent()
critic = CriticAgent()
connector = KnowledgeConnectorAgent()

def scout_node(state: AgentState):
    print("--- SCOUTING ---")
    res = scout.run(state["query"])
    return {"results": res.get("matches", [])}

def critic_node(state: AgentState):
    print("--- CRITIC VALIDATION ---")
    valid_matches = []
    for match in state["results"]:
        validation = critic.run(state["query"], match)
        if validation["is_valid"]:
            match["critic_score"] = validation["score"]
            match["critique"] = validation["critique"]
            valid_matches.append(match)
    return {"validated_results": valid_matches}

def connector_node(state: AgentState):
    print("--- CONNECTING KNOWLEDGE ---")
    final_results = []
    for match in state["validated_results"]:
        synergy = connector.run(state["query"], match)
        match["synergies"] = synergy
        final_results.append(match)
    return {"final_output": {"experts": final_results}}

# Costruzione del Grafo
workflow = StateGraph(AgentState)

workflow.add_node("scout", scout_node)
workflow.add_node("critic", critic_node)
workflow.add_node("connector", connector_node)

workflow.set_entry_point("scout")
workflow.add_edge("scout", "critic")
workflow.add_edge("critic", "connector")
workflow.add_edge("connector", END)

app_graph = workflow.compile()
