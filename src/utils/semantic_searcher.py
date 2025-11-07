import numpy as np
from sentence_transformers import SentenceTransformer
from src.services.pdf_processor import PDFProcessor

class SemanticSearcher:
    def __init__(self, pdf_path):
        self.pdf_processor = PDFProcessor(pdf_path)
        self.documents = self.pdf_processor.create_knowledge_base()
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.embeddings = self._create_embeddings()
    
    def _create_embeddings(self):
        """Cria os vetores de significado para todo o manual"""
        print("Criando embeddings para o manual...")
        return self.model.encode(self.documents)
    
    def search(self, query, top_k=3):
        """Encontra os trechos mais relevantes do manual"""
        # Transforma a pergunta em vetor
        query_embedding = self.model.encode([query])
        
        # Calcula similaridade com todos os trechos
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        
        # Pega os top_k mais relevantes
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        return [self.documents[i] for i in top_indices]

# Exemplo de uso simples
if __name__ == "__main__":
    searcher = SemanticSearcher("dados/Manual-Detalhado-Portal-do-Paciente.pdf")
    
    perguntas_teste = [
        "Como agendar teleconsulta?",
        "Esqueci minha senha",
        "Não consigo acessar a consulta",
        "Quais os horários de atendimento?"
    ]
    
    for pergunta in perguntas_teste:
        print(f"\n🔍 Pergunta: {pergunta}")
        resultados = searcher.search(pergunta)
        print(f"📄 Trechos encontrados: {len(resultados)}")
        for i, resultado in enumerate(resultados, 1):
            print(f"{i}. {resultado[:100]}...")