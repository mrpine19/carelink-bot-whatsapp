import os
import sys
import pickle
# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sentence_transformers import SentenceTransformer
from src.services.pdf_processor import PDFProcessor

def create_and_save_embeddings(pdf_path, output_path):
    """
    Lê um PDF, gera embeddings para seu conteúdo e salva os embeddings e os documentos em um arquivo.
    """
    print("1. Processando o PDF...")
    # Garante que o PDFProcessor use o caminho correto
    processor = PDFProcessor(pdf_path)
    documents = processor.create_knowledge_base()
    
    if not documents:
        print("Nenhum documento foi extraído do PDF. Verifique o processador.")
        return

    print(f"2. PDF processado. {len(documents)} trechos de texto foram criados.")
    
    print("3. Carregando o modelo de embedding ('all-MiniLM-L6-v2')...")
    # Carrega o modelo leve
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("4. Gerando os embeddings para os trechos de texto...")
    # Gera os embeddings
    embeddings = model.encode(documents, show_progress_bar=True)
    
    print("5. Salvando os embeddings e os documentos...")
    # Salva os documentos e seus embeddings em um único arquivo
    with open(output_path, "wb") as f:
        pickle.dump({'documents': documents, 'embeddings': embeddings}, f)
        
    print(f"✅ Embeddings e documentos salvos com sucesso em '{output_path}'!")

if __name__ == "__main__":
    # Define o caminho para o PDF e onde o arquivo de embeddings será salvo
    # O PDF está na pasta 'data/manuals' a partir da raiz do projeto
    pdf_file_path = "data/manuals/Manual-Detalhado-Portal-do-Paciente.pdf"
    # O arquivo de embeddings será salvo na pasta 'data'
    output_file_path = "data/manual_embeddings.pkl"
    
    # Garante que o caminho do PDF é relativo à raiz do projeto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    full_pdf_path = os.path.join(project_root, pdf_file_path)
    full_output_path = os.path.join(project_root, output_file_path)

    if not os.path.exists(full_pdf_path):
        print(f"Erro: O arquivo PDF não foi encontrado em '{full_pdf_path}'")
    else:
        create_and_save_embeddings(full_pdf_path, full_output_path)
