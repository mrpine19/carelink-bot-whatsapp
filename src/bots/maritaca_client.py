import openai
from src.utils.prompts import prompt_baixa_afinidade

class MaritacaClient:
    def __init__(self, api_key):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://chat.maritaca.ai/api"
        )
    
    def generate_response(self, prompt, context=None):
        messages = [
            {
                "role": "system", 
                "content": prompt_baixa_afinidade.format(
                    pergunta=prompt,
                    contexto=context if context else "Nenhum contexto adicional"
                )
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="sabia-3",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return self._fallback_response(prompt, context, e)
    
    def _fallback_response(self, prompt, context, error):
        """Resposta de fallback caso a API falhe"""
        print(f"Erro na Maritaca: {error}")
        
        # Respostas pré-definidas em linguagem simples
        respostas_simples = {
            "microfone": "Clique no ícone do microfone, é o desenho redondo com ondinhas",
            "senha": "Vá em 'Esqueci minha senha', digite seu CPF e siga as instruções no email",
            "agendar": "No menu principal, clique em 'Agendar', escolha a especialidade, depois a data e horário",
            "consulta": "Vá em 'Minhas consultas' e clique na consulta que quer ver os detalhes",
            "login": "Digite seu CPF no primeiro campo e sua senha no segundo campo, depois clique em 'Entrar'"
        }
        
        # Tenta encontrar resposta pré-definida
        prompt_lower = prompt.lower()
        for palavra, resposta in respostas_simples.items():
            if palavra in prompt_lower:
                return resposta
        
        # Resposta genérica de fallback
        return "Desculpe, estou com dificuldades técnicas no momento. Por favor, tente novamente mais tarde ou ligue para nossa central de atendimento."