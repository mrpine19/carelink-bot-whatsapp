import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class SemanticSearcher:
    def __init__(self, embeddings_path):
        """
        Inicializa o buscador semântico carregando os embeddings e documentos pré-calculados.
        """
        self.documents, self.embeddings = self._load_embeddings(embeddings_path)
        # O modelo ainda é necessário para vetorizar a PERGUNTA do usuário em tempo real.
        # No entanto, o processo de vetorizar o manual inteiro (que consome muita memória) não é mais feito aqui.
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _load_embeddings(self, file_path):
        """Carrega os embeddings e documentos de um arquivo."""
        print(f"Carregando embeddings pré-calculados de '{file_path}'...")
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        print("Embeddings carregados com sucesso.")
        return data['documents'], data['embeddings']

    def search(self, query, top_k=3):
        """
        Encontra os trechos mais relevantes do manual com base na pergunta do usuário.
        """
        # 1. Transforma a pergunta do usuário em um vetor (embedding)
        query_embedding = self.model.encode([query])
        
        # 2. Calcula a similaridade entre o vetor da pergunta e os vetores do manual
        #    np.dot é uma operação matemática muito rápida para isso.
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        
        # 3. Pega os 'top_k' trechos mais similares
        #    argsort() retorna os índices dos valores ordenados, e pegamos os últimos 'top_k'.
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        # 4. Retorna os documentos correspondentes a esses índices
        return [self.documents[i] for i in top_indices]

# Exemplo de uso (opcional, para teste local)
if __name__ == "__main__":
    # O caminho para o arquivo de embeddings gerado pelo script create_embeddings.py
    embeddings_file = "data/manual_embeddings.pkl"
    
    # Inicializa o buscador com os embeddings pré-calculados
    searcher = SemanticSearcher(embeddings_file)
    
    # Lista de perguntas para testar a busca
    perguntas_teste = [
        "Como agendar teleconsulta?",
        "Esqueci minha senha",
        "Não consigo acessar a consulta",
        "Quais os horários de atendimento?"
    ]
    
    # Itera sobre as perguntas e exibe os resultados da busca
    for pergunta in perguntas_teste:
        print(f"\n🔍 Pergunta: {pergunta}")
        resultados = searcher.search(pergunta)
        print(f"📄 Trechos encontrados: {len(resultados)}")
        for i, resultado in enumerate(resultados, 1):
            # Exibe os primeiros 100 caracteres de cada resultado
            print(f"{i}. {resultado[:100]}...")
