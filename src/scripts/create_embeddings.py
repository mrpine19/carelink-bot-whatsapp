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
    processor = PDFProcessor(pdf_path)
    documents = processor.create_knowledge_base()
    
    if not documents:
        print("Nenhum documento foi extraído do PDF. Verifique o processador.")
        return

    print(f"2. PDF processado. {len(documents)} trechos de texto foram criados.")
    
    print("3. Carregando o modelo de embedding ('all-MiniLM-L6-v2')...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("4. Gerando os embeddings para os trechos de texto...")
    embeddings = model.encode(documents, show_progress_bar=True)
    
    print("5. Salvando os embeddings e os documentos...")
    # Garante que o diretório de saída exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump({'documents': documents, 'embeddings': embeddings}, f)
        
    print(f"✅ Embeddings e documentos salvos com sucesso em '{output_path}'!")

if __name__ == "__main__":
    # Define o caminho para o PDF e onde o arquivo de embeddings será salvo
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # O PDF continua na pasta 'data' original
    pdf_file_path = os.path.join(project_root, "data", "manuals", "Manual-Detalhado-Portal-do-Paciente.pdf")
    
    # *** O ARQUIVO DE SAÍDA AGORA SERÁ SALVO DENTRO DA PASTA 'src' ***
    output_file_path = os.path.join(project_root, "src", "data", "manual_embeddings.pkl")

    if not os.path.exists(pdf_file_path):
        print(f"Erro: O arquivo PDF não foi encontrado em '{pdf_file_path}'")
    else:
        create_and_save_embeddings(pdf_file_path, output_file_path)
