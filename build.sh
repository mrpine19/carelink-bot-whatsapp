#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--- Iniciando Build ---"

# 1. Instalação de dependências
pip install --upgrade pip
pip install -r requirements.txt

# 2. Diagnóstico de Arquivos (Prova irrefutável)
# Lista todos os arquivos no projeto, de forma recursiva.
# Isso nos mostrará nos logs se o manual_embeddings.pkl está presente.
echo "--- Listando todos os arquivos no projeto ---"
ls -R

echo "--- Build Concluído com Sucesso ---"
