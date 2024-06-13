import os
import json
from datetime import datetime
from bot_instance import bot
from gradio_client import Client 
import time

# Definindo o cliente Gradio
client = Client("https://lukz770-chat-luna.hf.space")

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

        return result
        
# Função para simular a ação de digitação
def send_typing_action(chat_id):
    bot.send_chat_action(chat_id=chat_id, action='typing')
    time.sleep(1)
