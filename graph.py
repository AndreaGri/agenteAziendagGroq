import streamlit as st
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from agents.scout import ScoutAgent
from agents.critic import CriticAgent
from agents.connector import KnowledgeConnectorAgent

class AgentState(TypedDict):
    query: str
    results: List[dict]
    validated_results: List[dict]
    final_output: dict

scout = ScoutAgent()
critic = CriticAgent()
connector = KnowledgeConnectorAgent()

def scout_node(state: AgentState):
    st.write("🔍 **Agente Scout**: Sto cercando i profili migliori nel database...")
    res = scout.run(state["query"])
    return {"results": res.get("matches", [])}

def critic_node(state: AgentState):
    st.write(f"⚖️ **Agente Critic**: Valuto la pertinenza di {len(state['results'])} risultati...")
    valid_matches = []
    for match in state["results"]:
        validation = critic.run(state["query"], match)
        if validation["is_valid"] and validation["score"] >= 5:
            match["critic_score"] = validation["score"]
            match["critique"] = validation["critique"]
            valid_matches.append(match)
    return {"validated_results": valid_matches}

def connector_node(state: AgentState):
    st.write("🔗 **Agente Connector**: Identifico sinergie aziendali...")
    final_experts = []
    for match in state["validated_results"]:
        synergy = connector.run(state["query"], match)
        match["synergies"] = synergy
        final_experts.append(match)
    return {"final_output": {"experts": final_experts}}

workflow = StateGraph(AgentState)
workflow.add_node("scout", scout_node)
workflow.add_node("critic", critic_node)
workflow.add_node("connector", connector_node)

workflow.set_entry_point("scout")
workflow.add_edge("scout", "critic")
workflow.add_edge("critic", "connector")
workflow.add_edge("connector", END)

app_graph = workflow.compile()
