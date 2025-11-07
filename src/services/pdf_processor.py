import PyPDF2
import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.documents = []
    
    def extract_text_from_pdf(self):
        """Extrai texto do PDF manual do sistema"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                
                return text
        except Exception as e:
            print(f"Erro ao ler PDF: {e}")
            return ""
    
    def create_knowledge_base(self):
        """Cria base de conhecimento a partir do PDF"""
        text = self.extract_text_from_pdf()
        
        if not text:
            return []
        
        # Dividir o texto em chunks menores
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        documents = text_splitter.split_text(text)
        return documents

# Exemplo de uso
if __name__ == "__main__":
    processor = PDFProcessor("dados/Manual-Detalhado-Portal-do-Paciente.pdf")
    knowledge_base = processor.create_knowledge_base()
    print(f"Base de conhecimento criada com {len(knowledge_base)} segmentos")