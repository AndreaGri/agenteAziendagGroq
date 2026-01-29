import streamlit as st
import os
from database_manager import db_manager
from agents.parser import DocumentParserAgent
from graph import app_graph

st.set_page_config(page_title="AI Human Capital", layout="wide")

st.title("🚀 AI Sistema Valorizzazione Capitale Umano")
st.sidebar.header("Caricamento Documenti")

# Sezione Upload
uploaded_file = st.sidebar.file_uploader("Carica CV o Paper (PDF)", type="pdf")
if uploaded_file:
    with open(f"data/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.sidebar.button("Ingerisci Documento"):
        with st.spinner("Analisi in corso..."):
            parser = DocumentParserAgent()
            data = parser.run(f"data/{uploaded_file.name}")
            db_manager.add_profile(data)
            st.sidebar.success(f"Profilo di {data['name']} salvato!")

# Sezione Chat / Ricerca
query = st.text_input("Cerca un esperto (es: 'Chi sa usare la spettroscopia IR a Milano?')")

if query:
    with st.spinner("L'Orchestratore sta consultando gli agenti..."):
        # Esecuzione del Grafo
        inputs = {"query": query}
        result = app_graph.invoke(inputs)
        
        experts = result.get("final_output", {}).get("experts", [])
        
        if not experts:
            st.warning("Nessun esperto trovato con criteri sufficientemente validi.")
        else:
            for exp in experts:
                with st.expander(f"👤 {exp['name']} (Score: {exp['critic_score']}/10)"):
                    st.write(f"**Skills:** {exp['skills']}")
                    st.write(f"**Giudizio Critic:** {exp['critique']}")
                    st.divider()
                    st.subheader("💡 Sinergie e Opportunità")
                    st.write(exp['synergies']['suggested_collaborations'])
                    st.json(exp['synergies']['potential_projects'])

