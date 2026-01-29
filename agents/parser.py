import os
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

class SkillExtraction(BaseModel):
    name: str = Field(description="Nome della persona")
    skills: List[str] = Field(description="Lista competenze")
    experience_level: str = Field(description="Seniority")
    summary: str = Field(description="Sintesi")

class DocumentParserAgent:
    def __init__(self):
        self.llm = ChatOllama(model=os.getenv("MODEL_NAME"), temperature=0, format="json")
        self.parser = JsonOutputParser(pydantic_object=SkillExtraction)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei un parser HR. Estrai i dati in formato JSON."),
            ("user", "Documento: {text}\n{format_instructions}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

    def run(self, file_path: str):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        full_text = " ".join([d.page_content for d in docs])
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"text": full_text})
