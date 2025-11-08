import os
from flask import Flask, request, jsonify
from src.bots.carelink_bot import CareLinkBot

# --- CONFIGURAÇÃO ROBUSTA DE CAMINHOS ---
# Constrói um caminho absoluto para a raiz do projeto, não importa de onde o script seja chamado.
# __file__ -> /path/to/project/src/api_server.py
# os.path.dirname(__file__) -> /path/to/project/src
# os.path.dirname(...) -> /path/to/project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMBEDDINGS_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "manual_embeddings.pkl")

# --- LEITURA DAS CHAVES DE AMBIENTE ---
MARITACA_API_KEY = os.getenv("MARITACA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not MARITACA_API_KEY or not GEMINI_API_KEY:
    raise ValueError("As variáveis de ambiente MARITACA_API_KEY e GEMINI_API_KEY não foram configuradas.")

# --- INICIALIZAÇÃO DO BOT COM TRATAMENTO DE ERROS ---
app = Flask(__name__)
bot = None

try:
    print("--- Inicializando o CareLinkBot ---")
    print(f"Tentando carregar embeddings de: {EMBEDDINGS_FILE_PATH}")
    
    # Verifica se o arquivo existe ANTES de tentar inicializar o bot
    if not os.path.exists(EMBEDDINGS_FILE_PATH):
        raise FileNotFoundError(f"Arquivo de embeddings não encontrado no caminho: {EMBEDDINGS_FILE_PATH}")

    bot = CareLinkBot(
        maritaca_api_key=MARITACA_API_KEY,
        gemini_api_key=GEMINI_API_KEY,
        embeddings_path=EMBEDDINGS_FILE_PATH
    )
    print("--- CareLinkBot inicializado com sucesso ---")
except Exception as e:
    # Se qualquer erro ocorrer durante a inicialização, logamos e impedimos o app de rodar sem o bot.
    print(f"FATAL: Falha ao inicializar o CareLinkBot. A aplicação não pode iniciar. Erro: {e}")
    # Em um cenário de produção, isso poderia enviar um alerta.
    bot = None # Garante que o bot não esteja parcialmente inicializado

# --- ENDPOINTS DA API ---
@app.route("/ask", methods=["POST"])
def handle_ask():
    if bot is None:
        return jsonify({"error": "O serviço não está disponível no momento devido a um erro de inicialização."}), 503

    data = request.get_json()
    if not data or "userId" not in data or "question" not in data:
        return jsonify({"error": "Payload JSON inválido. 'userId' e 'question' são obrigatórios."}), 400

    user_id = data.get("userId")
    question = data.get("question")
    response_text = bot.handle_message(user_id, question)
    return jsonify({"answer": response_text})

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint de health check para o Render."""
    if bot is not None:
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "error", "reason": "Bot not initialized"}), 503

if __name__ == "__main__":
    # Roda o servidor apenas se o bot foi inicializado com sucesso
    if bot:
        app.run(host='0.0.0.0', port=5000)
    else:
        print("Aplicação não iniciada devido a falha na inicialização do bot.")
