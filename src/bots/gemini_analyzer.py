from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import base64

class GeminiAnalyzer:
    def __init__(self, api_key):
        self.llm = ChatGoogleGenerativeAI(
            api_key=api_key,
            model="gemini-pro-vision"  # Modelo para análise de imagens
        )
    
    def analyze_app_screenshot(self, image_data):
        """
        Analisa screenshots do aplicativo de teleconsulta
        e identifica problemas comuns
        """
        try:
            # Codificar imagem para base64
            if isinstance(image_data, str):
                # Se for caminho de arquivo
                with open(image_data, "rb") as image_file:
                    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                # Se já for dados binários
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prompt específico para análise de apps hospitalares
            prompt = """
            Analise esta screenshot do aplicativo de teleconsulta do Hospital das Clínicas.
            
            Identifique:
            1. Qual tela do aplicativo é esta?
            2. Há algum erro ou problema visível?
            3. O que o usuário está tentando fazer?
            4. Sugestão de solução baseada no manual
            
            Principais telas do app:
            - Login/autenticação
            - Agendamento de consultas 
            - Lista de consultas
            - Tela de consulta virtual
            - Configurações/perfil
            
            Principais problemas comuns:
            - Campos de login incorretos
            - Consulta não aparecendo
            - Erro de conexão
            - Botões não funcionais
            - Mensagens de erro específicas
            
            Seja objetivo e direto na análise.
            """
            
            # Criar mensagem para análise
            message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            )
            
            response = self.llm.invoke([message])
            return response.content
            
        except Exception as e:
            return f"Erro na análise da imagem: {str(e)}"
    
    def extract_text_from_image(self, image_data):
        """
        Extrai texto de imagens (útil para mensagens de erro)
        """
        try:
            if isinstance(image_data, str):
                with open(image_data, "rb") as image_file:
                    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            prompt = "Extraia TODO o texto visível desta imagem exatamente como aparece."
            
            message = HumanMessage(
                content=[
                    {
                        "type": "text", 
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            )
            
            response = self.llm.invoke([message])
            return response.content
            
        except Exception as e:
            return f"Erro na extração de texto: {str(e)}"