import os
from langchain_ollama import ChatOllama
from database_manager import db_manager
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

class ScoutResult(BaseModel):
    reasoning: str = Field(description="Ragionamento dello scout")
    matches: List[dict] = Field(description="Lista dei profili")

class ScoutAgent:
    def __init__(self):
        # Aggiunto default "llama3" per evitare l'errore NoneType
        model = os.getenv("MODEL_NAME", "llama3")
        self.llm = ChatOllama(model=model, temperature=0, format="json")
        self.db = db_manager
        self.parser = JsonOutputParser(pydantic_object=ScoutResult)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei l'Agente Scout. Analizza i profili e rispondi in JSON."),
            ("user", "Query: {query}\nRisultati: {results}\n{format_instructions}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

    def run(self, user_query: str):
        search_results = self.db.search_experts(user_query, k=3)
        formatted_results = [{"name": d.metadata.get("name"), "skills": d.metadata.get("skills")} for d, s in search_results]
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"query": user_query, "results": formatted_results})
