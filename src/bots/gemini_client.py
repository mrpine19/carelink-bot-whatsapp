from langchain_google_genai import ChatGoogleGenerativeAI
from src.utils.prompts import prompt_baixa_afinidade

class GeminiClient:
    def __init__(self, api_key):
        self.llm = ChatGoogleGenerativeAI(
            api_key=api_key,
            model="gemini-1.5-pro",  
            temperature=0.7
        )
    
    def generate_response_for_elderly(self, pergunta, contexto=None):
        
        prompt_final = prompt_baixa_afinidade.format(pergunta=pergunta)
        
        if contexto:
            prompt_final += f"\nCONTEXTO DO MANUAL: {contexto}"
        
        try:
            resposta = self.llm.invoke(prompt_final)
            return resposta.content
        except Exception as e:
            return f"Tente novamente. Deu erro: {str(e)}"