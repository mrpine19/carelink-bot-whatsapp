#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- [BUILD SCRIPT] Iniciando Build ---"
echo "--- [BUILD SCRIPT] Diretório de Trabalho Atual: $(pwd)"

# Criar diretório para cache do modelo SentenceTransformer
echo "--- [BUILD SCRIPT] Criando diretório de cache para modelos em /tmp/model_cache ---"
mkdir -p /tmp/model_cache

echo "--- [BUILD SCRIPT] Listando conteúdo do diretório raiz (recursivamente) ---"
find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'

echo "--- [BUILD SCRIPT] Verificando a existência do arquivo de embeddings ---"
EMBEDDINGS_PATH="data/manual_embeddings.pkl"

if [ -f "$EMBEDDINGS_PATH" ]; then
    echo "✅ [BUILD SCRIPT] SUCESSO: Arquivo de embeddings encontrado em '$EMBEDDINGS_PATH'."
    echo "   Tamanho do arquivo: $(du -h $EMBEDDINGS_PATH | cut -f1)"
else
    echo "❌ [BUILD SCRIPT] FALHA: Arquivo de embeddings NÃO encontrado em '$EMBEDDINGS_PATH'."
    echo "   Esta é a causa raiz do erro de inicialização. Verifique se o arquivo foi commitado no Git."
    # Não vamos falhar o build aqui, pois o api_server.py lida com isso em modo degradado.
fi

echo "--- [BUILD SCRIPT] Instalando dependências Python ---"
pip install --upgrade pip
pip install -r requirements.txt

echo "--- [BUILD SCRIPT] Build Concluído com Sucesso ---"
