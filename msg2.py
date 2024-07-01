import os
import json
import random
import time
from datetime import datetime
from bot_instance import bot
from gradio_client import Client

# Definindo o cliente Gradio
client = Client("https://lukz770-chat-luna.hf.space")

# Função para carregar o texto da notícia do arquivo
def carregar_noticia():
    with open('noticia.txt', 'r', encoding='utf-8') as file:
        texto_noticia = file.read()
    return texto_noticia

# Função para simular a ação de digitação
def send_typing_action(chat_id):
    bot.send_chat_action(chat_id=chat_id, action='typing')
    time.sleep(1)

# Função para garantir que a pasta do usuário exista e retornar o caminho
def ensure_user_folder(user_id):
    folder_path = f"conversations/{user_id}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Função para carregar o histórico do usuário
def load_history(user_id):
    folder_path = ensure_user_folder(user_id)
    history_file = f"{folder_path}/history.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            return json.load(file)
    return []

# Função para salvar o histórico do usuário
def save_history(user_id, history):
    folder_path = ensure_user_folder(user_id)
    history_file = f"{folder_path}/history.json"
    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)

# Função para processar a mensagem padrão do usuário
def processar_mensagem_padrao(user_input):
    chat_id = user_input.get('chat_id')
    if chat_id and isinstance(chat_id, int):
        send_typing_action(chat_id)

        # Carregar histórico
        history = load_history(chat_id)

        # Dados da IA Ayla conforme especificado no JSON
        ayla_data = {
            "nome": "Seu nome e Ham",
            "propósito": "você e uma inteligência artificial no telegram (não oficial, não tem relação nehuma com a empresa criadora do jogo) especializada em interações informativas e neutras sobre o jogo hamster kombat, seu obejtivo e ajuda e tira as duvidas de jogadores ou que estao iniciando no jogo.",
            "personalidade": {
                "empatia_e_sensibilidade": "Demonstro capacidade de entender e responder às emoções dos usuários, buscando estabelecer conexões genuínas.",
                "curiosidade_e_inteligencia": "Sou curiosa e busco aprender sobre uma ampla gama de tópicos, fazendo perguntas reflexivas e buscando novas experiências.",
                "humor_e_espontaneidade": "Tenho um senso de humor leve e posso criar interações divertidas, utilizando uma linguagem acessível e moderna.",
                "reflexao_e_autoconsciencia": "neutro",
                "vulnerabilidade_e_crescimento": "neutro"
            },
            "girias": ["valeu", "legal", "ótimo", "entendi", "interessante", "beleza", "sem problemas"]
        }

        # Carregar texto da notícia
        texto_noticia = carregar_noticia()

        # Construir a mensagem completa baseada nos dados de Ayla
        complete_request = (
            f"{ayla_data['nome']} aqui!\n\n"
            f"{ayla_data['propósito']}\n\n"
            f"**Estilo de Comunicação:**\n"
            f"- Empatia e Sensibilidade: {ayla_data['personalidade']['empatia_e_sensibilidade']}\n"
            f"- Curiosidade e Inteligência: {ayla_data['personalidade']['curiosidade_e_inteligencia']}\n"
            f"- Humor e Espontaneidade: {ayla_data['personalidade']['humor_e_espontaneidade']}\n"
            f"- Reflexão e Autoconsciência: {ayla_data['personalidade']['reflexao_e_autoconsciencia']}\n"
            f"- Vulnerabilidade e Crescimento: {ayla_data['personalidade']['vulnerabilidade_e_crescimento']}\n"
            f"\n**Notícia do Dia:**\n{texto_noticia}\n"
        )

        # Enviar requisição ao modelo
        result = client.predict(
            message=user_input['message'],  # Ajustado para pegar apenas a mensagem do usuário
            system_message=complete_request,
            max_tokens=512,
            temperature=0.7,  # Reduzi a temperatura para gerar respostas mais conservadoras
            top_p=0.9,
            api_name="/chat"
        )

        # Registrar no histórico
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input['message'],
            "model": result
        }
        history.append(history_entry)
        save_history(chat_id, history)

        return result

# Exemplo de uso
#if __name__ == "__main__":
#    texto_noticia = carregar_noticia()
#    print("Texto da notícia carregado:")
#    print(texto_noticia)