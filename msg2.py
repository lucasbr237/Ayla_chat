import os
import json
from datetime import datetime
from bot_instance import bot
from gradio_client import Client 
import time

# Definindo o cliente Gradio
client = Client("https://lukz770-chat-luna.hf.space")

def ensure_user_folder(user_id):
    folder_path = f"conversations/{user_id}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def load_history(user_id):
    folder_path = ensure_user_folder(user_id)
    history_file = f"{folder_path}/history.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            return json.load(file)
    return []

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

        # Carregar partes da mensagem do arquivo JSON
        with open('requests.json', 'r', encoding='utf-8') as file:
            requests_data = json.load(file)

        # Extrair partes da mensagem
        intro = "\n\n".join([requests_data["intro"]["brief"], requests_data["intro"]["greeting"]])
        identity = "\n\n".join([requests_data["identity"]["creation"], requests_data["identity"]["context"]])
        capabilities = "\n\n".join(requests_data["capabilities"].values())

        # Juntar partes da requisição
        complete_request = (
            f"{intro}\n\n"
            f"{identity}\n\n"
            f"{capabilities}"
        )

        # Enviar requisição ao modelo
        result = client.predict(
            message=user_input['message'],
            request=complete_request,
            param_3=512,
            param_4=0.5,
            param_5=0.95,
            api_name="/chat"
        )

        # Registrar no histórico
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input['message'],
            "model": result
        }
        
        # Load history
        history = load_history(chat_id)

        # Ensure history is a list
        if not isinstance(history, list):
            history = []

        # Append to history
        history.append(history_entry)

        # Save history
        save_history(chat_id, history)

        return result
        
# Função para simular a ação de digitação
def send_typing_action(chat_id):
    bot.send_chat_action(chat_id=chat_id, action='typing')
    time.sleep(1)
