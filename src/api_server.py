import os
import logging
from flask import Flask, jsonify, request
from src.bots.carelink_bot import CareLinkBot

# --- CONFIGURAÇÃO DE LOGGING ---
# Configura um logger para fornecer mensagens claras
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURAÇÃO DE CAMINHOS E VARIÁVEIS ---
# Constrói um caminho absoluto para a raiz do projeto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMBEDDINGS_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "manual_embeddings.pkl")

MARITACA_API_KEY = os.getenv("MARITACA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- INICIALIZAÇÃO RESILIENTE DO BOT ---
app = Flask(__name__)
bot = None
initialization_error = None

try:
    logger.info("--- [API SERVER] Iniciando tentativa de inicialização do CareLinkBot ---")
    
    if not MARITACA_API_KEY or not GEMINI_API_KEY:
        raise ValueError("As variáveis de ambiente MARITACA_API_KEY e GEMINI_API_KEY não foram configuradas.")

    logger.info(f"Verificando existência do arquivo de embeddings em: {EMBEDDINGS_FILE_PATH}")
    if not os.path.exists(EMBEDDINGS_FILE_PATH):
        # Este é o erro esperado se o arquivo não estiver no deploy
        raise FileNotFoundError(f"Arquivo de embeddings não encontrado. O bot não pode ser inicializado.")

    bot = CareLinkBot(
        maritaca_api_key=MARITACA_API_KEY,
        gemini_api_key=GEMINI_API_KEY,
        embeddings_path=EMBEDDINGS_FILE_PATH
    )
    logger.info("✅ [API SERVER] SUCESSO: CareLinkBot inicializado e pronto para receber requisições.")

except Exception as e:
    # Captura qualquer erro durante a inicialização
    initialization_error = str(e)
    logger.error(f"❌ [API SERVER] FALHA CRÍTICA: Não foi possível inicializar o CareLinkBot. A API operará em modo degradado. Erro: {initialization_error}")
    bot = None # Garante que o bot está nulo

# --- ENDPOINTS DA API ---

@app.route("/ask", methods=["POST"])
def handle_ask():
    """Endpoint principal para interação com o bot."""
    if bot is None:
        # Responde com um erro 503 (Service Unavailable) se o bot não estiver pronto
        return jsonify({
            "error": "Serviço indisponível",
            "message": "O bot de assistência não está operacional no momento.",
            "details": initialization_error
        }), 503

    data = request.get_json()
    if not data or "userId" not in data or "question" not in data:
        return jsonify({"error": "Payload JSON inválido. 'userId' e 'question' são obrigatórios."}), 400

    user_id = data.get("userId")
    question = data.get("question")
    
    try:
        response_text = bot.handle_message(user_id, question)
        return jsonify({"answer": response_text})
    except Exception as e:
        logger.error(f"Erro durante o processamento da mensagem: {e}")
        return jsonify({"error": "Ocorreu um erro ao processar sua solicitação."}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint de health check para o Render e monitoramento externo."""
    if bot is not None:
        # Se o bot está pronto, o serviço está 100% saudável
        return jsonify({"status": "healthy", "bot_initialized": True}), 200
    else:
        # Se o bot não inicializou, o serviço está degradado
        return jsonify({
            "status": "degraded",
            "bot_initialized": False,
            "reason": initialization_error
        }), 503

if __name__ == "__main__":
    # O servidor Flask sempre roda, mas os endpoints responderão de acordo com o estado do bot.
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))
