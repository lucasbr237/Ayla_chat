from bot_instance import bot
from gradio_client import Client 
import requests
import re
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import photo
from youtube import get_video_info
import menu_call
from msg2 import processar_mensagem_padrao

#variavel
last_bot2_message = None
def send_typing_action(chat_id):
    bot.send_chat_action(chat_id=chat_id, action='typing')
    time.sleep(1)  # Tempo de espera para simular digitação


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
                f"Canal: {video_info['channel_title']}\n"
                f"Visualizações: {video_info['views']}\n"
                f"Likes: {video_info['likes']}\n"
                f"Publicado em: {video_info['published_at']}\n"
                f"Duração: {video_info['duration']}\n"
            )

            # Verifica se há detalhes de live stream e adiciona à mensagem
            if 'actual_start_time' in video_info:
                live_info = (
                    f"Transmissão ao vivo:\n"
                    f"Início real: {video_info['actual_start_time']}\n"
                    f"Término real: {video_info['actual_end_time']}\n"
                    f"Visualizadores simultâneos: {video_info['concurrent_viewers']}\n"
                )
                info += live_info

            user_input['message'] = info  # Atualiza a mensagem do usuário com as informações do vídeo
            result = processar_mensagem_padrao(user_input)
        else:
            result = "Não foi possível encontrar informações para este vídeo."
    else:
        # Se não for um link do YouTube, processa a mensagem normalmente
        result = processar_mensagem_padrao(user_input)
    
    bot.reply_to(message, result)
