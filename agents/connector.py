import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

class SynergyResult(BaseModel):
    potential_projects: List[str] = Field(description="In quali tipi di progetti questo esperto darebbe valore?")
    suggested_collaborations: str = Field(description="Quali altri reparti dovrebbero contattarlo?")
    strategic_value: str = Field(description="Valore aggiunto unico per l'azienda")

class KnowledgeConnectorAgent:
    def __init__(self):
        self.llm = ChatGroq(temperature=0.3, model_name=os.getenv("MODEL_NAME"))
        self.parser = JsonOutputParser(pydantic_object=SynergyResult)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei l'Agente Knowledge Connector. Il tuo compito è identificare sinergie strategiche tra esperti e l'organizzazione. Non limitarti a ripetere le skill, pensa in modo creativo ma professionale."),
            ("user", "Profilo Esperto: {profile}\nRichiesta Aziendale: {query}\n\nIdentifica le sinergie in JSON.\n{format_instructions}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

    def run(self, query, profile):
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"query": query, "profile": profile})
