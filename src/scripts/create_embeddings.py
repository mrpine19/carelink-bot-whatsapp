import os
import sys
import pickle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sentence_transformers import SentenceTransformer
# Corrigindo o import para o novo local do PDFProcessor, se ele foi movido
from src.services.pdf_processor import PDFProcessor

def create_and_save_embeddings(pdf_path, output_path):
    print("1. Processando o PDF...")
    processor = PDFProcessor(pdf_path)
    documents = processor.create_knowledge_base()
    
    if not documents:
        print("Nenhum documento foi extraído do PDF.")
        return

    print(f"2. PDF processado. {len(documents)} trechos criados.")
    
    print("3. Carregando modelo 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("4. Gerando embeddings...")
    embeddings = model.encode(documents, show_progress_bar=True)
    
    # Garante que o diretório de saída exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"5. Salvando embeddings e documentos em '{output_path}'...")
    with open(output_path, "wb") as f:
        pickle.dump({'documents': documents, 'embeddings': embeddings}, f)
        
    print(f"✅ Salvo com sucesso!")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Caminho do PDF original
    pdf_file_path = os.path.join(project_root, "data", "manuals", "Manual-Detalhado-Portal-do-Paciente.pdf")
    
    # Caminho de saída na pasta 'data' na raiz do projeto
    output_file_path = os.path.join(project_root, "data", "manual_embeddings.pkl")

    if not os.path.exists(pdf_file_path):
        print(f"Erro: Arquivo PDF não encontrado em '{pdf_file_path}'")
    else:
        create_and_save_embeddings(pdf_file_path, output_file_path)
