import os
from flask import Flask, request, jsonify
# Importa sua classe e suas chaves usando a estrutura do seu projeto
from src.bots.carelink_bot import CareLinkBot

# --- LEITURA DAS CHAVES A PARTIR DAS VARIÁVEIS DE AMBIENTE ---
# No Render, você deve configurar estas variáveis no painel do seu serviço
MARITACA_API_KEY = os.getenv("MARITACA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not MARITACA_API_KEY or not GEMINI_API_KEY:
    raise ValueError("As variáveis de ambiente MARITACA_API_KEY e GEMINI_API_KEY não foram configuradas.")

# --- CONFIGURAÇÃO E INICIALIZAÇÃO DO BOT ---
print("Inicializando o CareLinkBot para o servidor API...")

# Instanciamos o bot UMA ÚNICA VEZ quando o servidor inicia.
bot = CareLinkBot(
    maritaca_api_key=MARITACA_API_KEY,
    gemini_api_key=GEMINI_API_KEY,
    pdf_path="data/manuals/Manual-Detalhado-Portal-do-Paciente.pdf"
)

print("CareLinkBot pronto. Servidor API iniciado.")
# ---------------------------------------------

# Cria a aplicação Flask
app = Flask(__name__)

# Define o endpoint '/ask' que a aplicação Java irá chamar
@app.route("/ask", methods=["POST"])
def handle_ask():
    data = request.get_json()
    if not data or "userId" not in data or "question" not in data:
        return jsonify({"error": "Payload JSON inválido. 'userId' e 'question' são obrigatórios."}), 400

    user_id = data.get("userId")
    question = data.get("question")

    print(f"API recebeu a pergunta de '{user_id}': '{question}'")

    # AQUI A MÁGICA ACONTECE:
    # A API simplesmente passa a pergunta para o método do seu bot
    response_text = bot.handle_message(user_id, question)

    print(f"API enviando a resposta: '{response_text}'")

    # Retorna a resposta para o Java no formato JSON combinado
    return jsonify({"answer": response_text})

# Roda o servidor
if __name__ == "__main__":
    # use host='0.0.0.0' para ser acessível por outras máquinas na mesma rede
    app.run(host='0.0.0.0', port=5000)