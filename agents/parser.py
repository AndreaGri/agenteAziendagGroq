import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

class SkillExtraction(BaseModel):
    name: str = Field(description="Nome della persona o del profilo")
    skills: List[str] = Field(description="Lista di competenze tecniche specifiche")
    experience_level: str = Field(description="Seniority (Junior, Middle, Senior, Expert)")
    summary: str = Field(description="Breve sintesi del valore professionale")

class DocumentParserAgent:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name=os.getenv("MODEL_NAME"))
        self.parser = JsonOutputParser(pydantic_object=SkillExtraction)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei un AI Parsing Engine specializzato in HR Tech. Il tuo compito è estrarre competenze granulari. Rispondi esclusivamente in formato JSON."),
            ("user", "Analizza il seguente documento ed estrai le informazioni: {text}\n{format_instructions}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

    def run(self, file_path: str):
        if not os.path.exists(file_path):
            return {"error": f"File {file_path} non trovato"}
        
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        full_text = " ".join([d.page_content for d in docs])
        
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"text": full_text})

