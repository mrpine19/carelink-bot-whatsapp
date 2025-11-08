import os
import logging
import gc
import psutil # Para diagnóstico de memória
from flask import Flask, jsonify, request
from src.bots.carelink_bot import CareLinkBot

# --- CONFIGURAÇÃO DE LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- FUNÇÃO DE DIAGNÓSTICO DE MEMÓRIA ---
def log_memory_usage(phase: str):
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    logger.info(f"[MEMORY DIAGNOSIS] {phase}: {memory_mb:.2f} MB")
    return memory_mb

# --- CONFIGURAÇÃO DE CAMINHOS E VARIÁVEIS ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMBEDDINGS_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "manual_embeddings.pkl")

MARITACA_API_KEY = os.getenv("MARITACA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- INICIALIZAÇÃO RESILIENTE DO BOT ---
app = Flask(__name__)
bot = None
initialization_error = None

log_memory_usage("Antes da inicialização do Flask e do bot")

try:
    logger.info("--- [API SERVER] Iniciando tentativa de inicialização do CareLinkBot ---")
    
    if not MARITACA_API_KEY or not GEMINI_API_KEY:
        raise ValueError("As variáveis de ambiente MARITACA_API_KEY e GEMINI_API_KEY não foram configuradas.")

    logger.info(f"Verificando existência do arquivo de embeddings em: {EMBEDDINGS_FILE_PATH}")
    if not os.path.exists(EMBEDDINGS_FILE_PATH):
        raise FileNotFoundError(f"Arquivo de embeddings não encontrado. O bot não pode ser inicializado.")

    # A inicialização do CareLinkBot agora é mais leve devido ao lazy loading no SemanticSearcher
    bot = CareLinkBot(
        maritaca_api_key=MARITACA_API_KEY,
        gemini_api_key=GEMINI_API_KEY,
        embeddings_path=EMBEDDINGS_FILE_PATH
    )
    log_memory_usage("Após a inicialização do CareLinkBot (sem carregar modelo/embeddings)")
    
    gc.collect() # Força a coleta de lixo após a inicialização
    logger.info("✅ [API SERVER] SUCESSO: CareLinkBot inicializado e pronto para receber requisições.")

except Exception as e:
    initialization_error = str(e)
    logger.error(f"❌ [API SERVER] FALHA CRÍTICA: Não foi possível inicializar o CareLinkBot. A API operará em modo degradado. Erro: {initialization_error}")
    bot = None

log_memory_usage("Após o bloco try/except de inicialização")

# --- ENDPOINTS DA API ---

@app.route("/ask", methods=["POST"])
def handle_ask():
    if bot is None:
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
        # A primeira chamada a search() aqui acionará o lazy loading do modelo e embeddings
        response_text = bot.handle_message(user_id, question)
        return jsonify({"answer": response_text})
    except Exception as e:
        logger.error(f"Erro durante o processamento da mensagem: {e}")
        return jsonify({"error": "Ocorreu um erro ao processar sua solicitação."}), 500

@app.route("/health", methods=["GET"])
def health_check():
    current_memory = log_memory_usage("Health Check")
    
    status_data = {
        "status": "healthy" if bot else "degraded",
        "bot_initialized": bot is not None,
        "reason": initialization_error,
        "memory_usage_mb": round(current_memory, 2)
    }
    
    if bot is None:
        return jsonify(status_data), 503
    else:
        return jsonify(status_data), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))
