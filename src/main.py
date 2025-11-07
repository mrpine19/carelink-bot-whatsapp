from src.bots.carelink_bot import CareLinkBot
from config.my_keys import MARITACA_API_KEY, GEMINI_API_KEY  

def main():
    # VOLTA parâmetro maritaca_api_key
    bot = CareLinkBot(
        maritaca_api_key=MARITACA_API_KEY,  
        gemini_api_key=GEMINI_API_KEY,
        pdf_path="C:/Dev/workspace/careLink-bot/data/manuals/Manual-Detalhado-Portal-do-Paciente.pdf"
    )
    
    questions = [
        "Como ligo meu microfone?",
        "obrigado"
    ]
    
    for question in questions:
        print(f"Paciente: {question}")
        response = bot.handle_message("12345", question)
        print(f"CareLink: {response}\n")

if __name__ == "__main__":
    main()