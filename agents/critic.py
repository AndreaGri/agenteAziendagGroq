import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class ValidationResult(BaseModel):
    is_valid: bool = Field(description="Il risultato è pertinente alla ricerca?")
    score: int = Field(description="Voto da 1 a 10 della pertinenza")
    critique: str = Field(description="Spiegazione della validazione o del perché è un falso positivo")

class CriticAgent:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name=os.getenv("MODEL_NAME"))
        self.parser = JsonOutputParser(pydantic_object=ValidationResult)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei l'Agente Critic. Il tuo compito è validare se i profili trovati corrispondono REALMENTE alla richiesta. Sii severo: se uno sa usare Python ma l'utente cerca Java, il risultato non è valido."),
            ("user", "Richiesta Utente: {query}\nProfilo Trovato: {profile}\n\nValuta la pertinenza in JSON.\n{format_instructions}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

    def run(self, query, profile):
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"query": query, "profile": profile})
