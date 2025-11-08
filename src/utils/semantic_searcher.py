import pickle
import os
import logging
from sentence_transformers import SentenceTransformer
import gc
import numpy as np

logger = logging.getLogger(__name__)

class SemanticSearcher:
    def __init__(self, embeddings_path):
        self.embeddings_path = embeddings_path
        self._model = None
        self._documents = None
        self._embeddings = None
        self._is_loaded = False
        logger.info(f"[SemanticSearcher] Inicializado com path: {embeddings_path}. Modelo e embeddings serão carregados sob demanda.")
        
    @property
    def model(self):
        """Carrega o modelo SentenceTransformer sob demanda (lazy loading)."""
        if self._model is None:
            logger.info("[SemanticSearcher] Carregando modelo SentenceTransformer 'all-MiniLM-L6-v2'...")
            # Configurações para minimizar uso de memória:
            # device='cpu' é padrão no Render, mas explícito é melhor.
            # cache_folder='/tmp/model_cache' para usar um diretório temporário.
            self._model = SentenceTransformer(
                'all-MiniLM-L6-v2',
                device='cpu',
                cache_folder='/tmp/model_cache'
            )
            gc.collect() # Força a coleta de lixo após carregar o modelo
            logger.info("[SemanticSearcher] Modelo SentenceTransformer carregado.")
        return self._model
    
    def _load_embeddings_on_demand(self):
        """Carrega os embeddings e documentos sob demanda."""
        if not self._is_loaded:
            logger.info(f"[SemanticSearcher] Carregando embeddings de '{self.embeddings_path}'...")
            
            if not os.path.exists(self.embeddings_path):
                raise FileNotFoundError(f"Arquivo de embeddings não encontrado: {self.embeddings_path}")
            
            with open(self.embeddings_path, "rb") as f:
                data = pickle.load(f)
            
            self._documents = data.get('documents', [])
            self._embeddings = data.get('embeddings', [])
            self._is_loaded = True
            
            logger.info(f"[SemanticSearcher] Embeddings carregados: {len(self._documents)} documentos.")
            
            # Liberar memória do objeto 'data' do pickle
            del data
            gc.collect() # Força a coleta de lixo
    
    def search(self, query, top_k=3):
        """Encontra os trechos mais relevantes do manual."""
        if not self._is_loaded:
            self._load_embeddings_on_demand()
        
        # Gerar embedding da query usando o modelo lazy-loaded
        query_embedding = self.model.encode([query])
        
        # Calcula similaridade
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        
        # Pega os top_k mais relevantes
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        return [self.documents[i] for i in top_indices]

    def unload_resources(self):
        """Libera o modelo e embeddings da memória, se carregados."""
        if self._model is not None:
            del self._model
            self._model = None
            logger.info("[SemanticSearcher] Modelo SentenceTransformer descarregado.")
        if self._embeddings is not None:
            del self._embeddings
            self._embeddings = None
            del self._documents
            self._documents = None
            self._is_loaded = False
            logger.info("[SemanticSearcher] Embeddings descarregados.")
        gc.collect()
