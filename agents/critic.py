import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class ValidationResult(BaseModel):
    is_valid: bool
    score: int
    critique: str

class CriticAgent:
    def __init__(self):
        model = os.getenv("MODEL_NAME", "llama3")
        self.llm = ChatOllama(model=model, temperature=0, format="json")
        self.parser = JsonOutputParser(pydantic_object=ValidationResult)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei l'Agente Critic. Valuta la pertinenza in JSON."),
            ("user", "Query: {query}\nProfilo: {profile}\n{format_instructions}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

    def run(self, query, profile):
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"query": query, "profile": profile})
