import chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

class DBManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db_path = os.getenv("DB_PATH", "./db/chroma_db")
        self.collection_name = "human_capital"
        self.client = chromadb.PersistentClient(path=self.db_path)
        
    def get_vectorstore(self):
        return Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embeddings
        )

    def add_profile(self, extracted_data):
        vectorstore = self.get_vectorstore()
        content = f"Nome: {extracted_data['name']}. Competenze: {', '.join(extracted_data['skills'])}. Sintesi: {extracted_data['summary']}"
        vectorstore.add_texts(
            texts=[content],
            metadatas=[{
                "name": extracted_data['name'],
                "seniority": extracted_data['experience_level'],
                "skills": ", ".join(extracted_data['skills'])
            }],
            ids=[str(uuid.uuid4())]
        )
        return True

    def search_experts(self, query, k=3):
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search_with_score(query, k=k)

db_manager = DBManager()
