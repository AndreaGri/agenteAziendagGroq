import streamlit as st
import os
from database_manager import db_manager
from agents.parser import DocumentParserAgent
from graph import app_graph

st.set_page_config(page_title="Local AI Human Capital", layout="wide")

st.title("🦙 Local AI - Valorizzazione Capitale Umano")
st.caption("Eseguito localmente su Ollama (Nessuna API Key richiesta)")

with st.sidebar:
    st.header("📁 Ingestione")
    uploaded_file = st.file_uploader("Carica CV (PDF)", type="pdf")
    if uploaded_file and st.button("Analizza"):
        path = f"data/{uploaded_file.name}"
        with open(path, "wb") as f: f.write(uploaded_file.getbuffer())
        with st.spinner("Ollama sta analizzando..."):
            parser = DocumentParserAgent()
            data = parser.run(path)
            db_manager.add_profile(data)
            st.success(f"Aggiunto: {data['name']}")

query = st.text_input("🔍 Cerca competenze nel team:", placeholder="Es: Chi conosce MongoDB?")

if query:
    with st.spinner("L'Orchestratore locale sta elaborando..."):
        result = app_graph.invoke({"query": query})
        experts = result.get("final_output", {}).get("experts", [])
        
        if not experts:
            st.warning("Nessun match trovato.")
        for exp in experts:
            with st.expander(f"👤 {exp['name']} (Score: {exp['critic_score']}/10)"):
                st.write(f"**Skills:** {exp['skills']}")
                st.info(f"**Analisi:** {exp['critique']}")
