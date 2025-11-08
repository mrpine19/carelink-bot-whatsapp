#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- [START SCRIPT] Iniciando a aplicação Gunicorn ---"

# Configurações de ambiente para otimização de memória
# PYTHONUNBUFFERED=TRUE: Garante que os logs do Python apareçam imediatamente.
# MALLOC_MMAP_THRESHOLD_ e MALLOC_TRIM_THRESHOLD_: Ajustam o comportamento do alocador de memória glibc
# para liberar memória de forma mais agressiva, o que pode ser útil em ambientes com pouca RAM.
export PYTHONUNBUFFERED=TRUE
export MALLOC_MMAP_THRESHOLD_=131072 # 128KB
export MALLOC_TRIM_THRESHOLD_=131072 # 128KB

# Executa o Gunicorn com configurações otimizadas para baixa memória:
# --workers 1: Um único processo worker para evitar duplicação de memória base.
# --threads 2: Reduzido de 4 para 2 threads por worker. Cada thread pode ter sua própria pilha,
#              e 2 é um bom ponto de partida para equilibrar concorrência e memória.
# --worker-class gthread: Usa threads Python.
# --bind 0.0.0.0:$PORT: Liga o servidor a todas as interfaces na porta especificada pelo Render.
# --timeout 120: Aumenta o tempo limite para requisições longas (ex: primeira requisição que carrega o modelo).
# --preload: Carrega a aplicação uma vez antes de fazer o fork dos workers. Isso permite que o modelo
#            SentenceTransformer seja carregado na memória do processo pai e compartilhado (copy-on-write)
#            com os workers, economizando memória.
# --log-level info: Define o nível de log.
exec gunicorn \
  --workers 1 \
  --threads 2 \
  --worker-class gthread \
  --bind 0.0.0.0:"$PORT" \
  --timeout 120 \
  --preload \
  --log-level info \
  src.api_server:app

echo "--- [START SCRIPT] Gunicorn encerrado ---"
