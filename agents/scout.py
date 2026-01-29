import os
from langchain_groq import ChatGroq
from database_manager import db_manager
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

class ScoutResult(BaseModel):
    reasoning: str = Field(description="Perché questi profili sono rilevanti?")
    matches: List[dict] = Field(description="Lista dei profili trovati con nome e skill")

class ScoutAgent:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name=os.getenv("MODEL_NAME"))
        self.db = db_manager
        self.parser = JsonOutputParser(pydantic_object=ScoutResult)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei l'Agente Scout. Il tuo compito è analizzare i profili trovati nel database e spiegare perché corrispondono alla query dell'utente. Sii tecnico e preciso."),
            ("user", "Query Utente: {query}\n\nProfili Estratti: {results}\n\nFornisci un'analisi in JSON.\n{format_instructions}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

    def run(self, user_query: str):
        # 1. Ricerca nel Vector DB
        search_results = self.db.search_experts(user_query, k=3)
        
        # 2. Formattazione risultati per l'LLM
        formatted_results = []
        for doc, score in search_results:
            formatted_results.append({
                "name": doc.metadata.get("name"),
                "skills": doc.metadata.get("skills"),
                "relevance_score": float(score)
            })
            
        # 3. Ragionamento dell'Agente Scout tramite LLM
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"query": user_query, "results": formatted_results})

