import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import uuid

class DBManager:
    def __init__(self):
        # Utilizziamo embeddings locali (leggeri)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db_path = "./db/chroma_db"
        # Inizializziamo il client persistente di Chroma
        self.client = chromadb.PersistentClient(path=self.db_path)
        
    def get_vectorstore(self):
        # Nuovo modo di inizializzare Chroma con LangChain 0.2+
        return Chroma(
            client=self.client, 
            collection_name="human_capital", 
            embedding_function=self.embeddings
        )

    def add_profile(self, extracted_data, owner_id="System"):
        vectorstore = self.get_vectorstore()
        # Creiamo un testo descrittivo per l'indicizzazione
        content = f"Nome: {extracted_data['name']}. Competenze: {', '.join(extracted_data['skills'])}. Seniority: {extracted_data['experience_level']}"
        
        # Aggiungiamo i metadati completi per le ricerche future
        vectorstore.add_texts(
            texts=[content], 
            metadatas=[{**extracted_data, "owner": owner_id}], 
            ids=[str(uuid.uuid4())]
        )
        return True

    def search_experts(self, query, k=3):
        return self.get_vectorstore().similarity_search_with_score(query, k=k)

db_manager = DBManager()
