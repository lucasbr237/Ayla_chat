from bot_instance import bot
from gradio_client import Client 
import requests
import re
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import photo
from youtube import get_video_info
# Inicializa o cliente do Gradio
client = Client("https://lukz770-chat-luna.hf.space")

def processar_mensagem_padrao(user_input):
    if 'chat_id' in user_input and isinstance(user_input['chat_id'], int):  # Verifica se 'chat_id' é um inteiro
        send_typing_action(user_input['chat_id'])  # Envie a ação de digitação ao usuário
        
        # Partes da request
        request_part1 = "You are Ayla, Chatbot, and you speak Portuguese."
        request_part2 = "Apresente-se."
        request_part3 = "Você é Ayla + Modelo LLM: Meta-Llama-3-8B-Instruct, adaptada por @lukasz99."
        request_part4 = "Ayla + Função, Você Descreve fotos."
        request_part5 = "Ayla + Funçao, Você Resume + Listar informações de videos do youtube."
        request_part6 = "Você pode fornecer informações detalhadas."
        request_part7 = "Você pode ajudar com traduções."
        request_part8 = "/Nw +Mudar de assunto."
        request_part9 = "Você pode oferecer conselhos."
        
        # Combina as partes da request
        complete_request = (
            f"{request_part1}\n\n---\n\n{request_part2}\n\n{request_part3}\n\n"
            f"{request_part4}\n\n{request_part5}\n\n{request_part6}\n\n"
            f"{request_part7}\n\n{request_part8}\n\n{request_part9}"
        )
        result = client.predict(
            message=user_input['message'],
            request=complete_request,
            param_3=512,
            param_4=0.5,
            param_5=0.95,
            api_name="/chat"
        )
        return result
    

def send_typing_action(chat_id):
    bot.send_chat_action(chat_id=chat_id, action='typing')
    time.sleep(1)  # Tempo de espera para simular digitação

# Função para lidar com mensagens de texto
@bot.message_handler(commands=['start'])
def handle_start(message):
    send_menu_message(message.chat.id)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_input = {
        'chat_id': message.chat.id,
        'message': message.text
    }
    # Verifica se o texto é um link do YouTube
    video_id = re.search(r'(?<=v=)[\w-]+|(?<=be/)[\w-]+', user_input['message'])
    if video_id:
        video_id = video_id.group(0)
        video_info = get_video_info(video_id)
        if video_info:
            # Passa as informações do vídeo para Ayla
            info = (
                f"Informações do vídeo:\n"
                f"Título: {video_info['title']}\n"
                f"Visualizações: {video_info['views']}\n"
                f"Likes: {video_info['likes']}\n"
            )
            user_input['message'] = info  # Atualiza a mensagem do usuário com as informações do vídeo
            result = processar_mensagem_padrao(user_input)
        else:
            result = "Não foi possível encontrar informações para este vídeo."
    else:
        # Se não for um link do YouTube, processa a mensagem normalmente
        result = processar_mensagem_padrao(user_input)
    
    bot.reply_to(message, result)
