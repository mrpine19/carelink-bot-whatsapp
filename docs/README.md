![](https://img.shields.io/badge/Python-3.8%2B-blue)
![](https://img.shields.io/badge/LangChain-0.3.7-green)
![](https://img.shields.io/badge/license-MIT-lightgrey)

# 🤖 CareLink - Assistente Digital para Redução de Absenteísmo

Solução inteligente de atendimento ao paciente desenvolvida para o Hospital das Clínicas, combinando IA generativa com o sistema de teleconsulta existente para reduzir absenteísmo em 20%.

## 🎯 Objetivo do Projeto

O CareLink é um assistente digital que ajuda pacientes com baixa afinidade digital a navegar no sistema de teleconsulta, fornece lembretes inteligentes e resolve dúvidas baseando-se no manual oficial do sistema.

## 🔨 Funcionalidades Principais

- **🤖 Assistente Conversacional** baseado em Maritaca AI com contexto cultural brasileiro
- **📄 Análise de Documentos** processamento do manual do sistema via PDF
- **🖼️ Análise de Imagens** interpretação de screenshots usando Gemini AI
- **🔔 Sistema de Lembretes** integrado com sistema Java existente
- **🧠 Busca Semântica** entendimento contextual de perguntas dos pacientes

## 🏗️ Arquitetura do Sistema
CareLink Bot → Maritaca AI (conversas) → Gemini (análise visual) → Sistema Java (dados)
↓
Manual PDF (base de conhecimento)

text

## ✔️ Técnicas e Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **LangChain** - Framework para orquestração de LLMs
- **Maritaca AI** - Modelo de linguagem em português
- **Google Gemini** - Análise multimodal de imagens
- **Sentence Transformers** - Busca semântica em documentos
- **PyPDF2** - Processamento de manuais PDF

## 📦 Estrutura do Projeto
carelink-bot/
├── src/ # Código fonte
│ ├── bots/ # Módulos do bot
│ ├── services/ # Gerenciadores de serviço
│ └── utils/ # Utilitários
├── data/ # Dados e recursos
│ ├── manuals/ # Manuais PDF
│ └── images/ # Imagens para análise
├── config/ # Configurações
└── tests/ # Testes

text

## 🛠️ Abrir e Configurar o Projeto

### 1. Preparar Ambiente Virtual

**Windows:**
```bash
python -m venv venv-carelink
venv-carelink\Scripts\activate
Mac/Linux:

bash
python3 -m venv venv-carelink
source venv-carelink/bin/activate
2. Instalar Dependências
bash
pip install -r requirements.txt
3. Configurar Chaves de API
Crie um arquivo config/keys.py com:

python
GEMINI_API_KEY = "sua_chave_gemini_aqui"
MARITACA_API_KEY = "sua_chave_maritaca_aqui"
4. Adicionar Manual do Sistema
Coloque o manual PDF em: data/manuals/Manual-Detalhado-Portal-do-Paciente.pdf

5. Executar o Projeto
bash
python -m src.main
🚀 Como Usar
Exemplo de Interação:
python
from src.bots.carelink_bot import CareLinkBot

bot = CareLinkBot(MARITACA_API_KEY, GEMINI_API_KEY, "caminho/do/manual.pdf")

# Pergunta textual
resposta = bot.handle_message("paciente123", "Como agendar teleconsulta?")
print(resposta)

# Análise de screenshot
with open("erro_login.png", "rb") as img:
    resposta = bot.handle_message("paciente123", "Veja esse erro", img.read())
    print(resposta)
📊 Resultados Esperados
Redução de 20% no absenteísmo por consultas

Diminuição de 35% nas dúvidas operacionais

Melhoria na experiência do paciente idoso

Integração transparente com sistema existente

👥 Responsabilidade
Desenvolvido para o NETI – Núcleo Especializado em Tecnologia da Informação do Hospital das Clínicas da Faculdade de Medicina da USP.

📄 Licença
Este projeto é de uso interno do Complexo HCFMUSP. É proibida a reprodução total ou parcial sem autorização do NETI.

💡 Dúvidas? Consulte o manual do sistema em data/manuals/ ou entre em contato com a equipe de desenvolvimento.

text

## 📝 Principais Mudanças Realizadas:

1. **✅ Título e descrição** atualizados para o projeto CareLink
2. **✅ Objetivo** focado na redução de absenteísmo do HC
3. **✅ Funcionalidades** específicas para o contexto hospitalar
4. **✅ Arquitetura** refletindo a integração com sistemas existentes
5. **✅ Tecnologias** mantidas mas com aplicação contextualizada
6. **✅ Estrutura** mostrando a nova organização de pastas
7. **✅ Instruções** adaptadas para o projeto real
8. **✅ Exemplos** de uso prático no contexto de telemedicina
9. **✅ Informações** institucionais do Hospital das Clínicas
10. **✅ Licença** conforme manual do sistema

O README agora está totalmente alinhado com seu projeto real do CareLink! Precisa de mais alguma ajuste?