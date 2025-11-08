import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class SemanticSearcher:
    def __init__(self, embeddings_path):
        """
        Inicializa o buscador semântico carregando os embeddings e documentos pré-calculados.
        A verificação da existência do arquivo é feita antes da inicialização.
        """
        self.documents, self.embeddings = self._load_embeddings(embeddings_path)
        # O modelo ainda é carregado para vetorizar a pergunta do usuário.
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _load_embeddings(self, file_path):
        """Carrega os embeddings e documentos de um arquivo."""
        print(f"Carregando embeddings de '{file_path}'...")
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        print("Embeddings carregados com sucesso.")
        return data['documents'], data['embeddings']

    def search(self, query, top_k=3):
        """
        Encontra os trechos mais relevantes do manual com base na pergunta do usuário.
        """
        query_embedding = self.model.encode([query])
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [self.documents[i] for i in top_indices]
