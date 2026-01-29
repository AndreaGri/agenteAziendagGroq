import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

class SynergyResult(BaseModel):
    potential_projects: List[str]
    suggested_collaborations: str

class KnowledgeConnectorAgent:
    def __init__(self):
        model = os.getenv("MODEL_NAME", "llama3")
        self.llm = ChatOllama(model=model, temperature=0.3, format="json")
        self.parser = JsonOutputParser(pydantic_object=SynergyResult)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei l'Agente Connector. Identifica sinergie in JSON."),
            ("user", "Profilo: {profile}\nQuery: {query}\n{format_instructions}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

    def run(self, query, profile):
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"query": query, "profile": profile})
