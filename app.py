from bot_instance import bot
from gradio_client import Client 
import requests
import re
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import photo
from youtube import get_video_info
from msg2 import processar_mensagem_padrao

def send_menu_message(chat_id):
    menu_message = (
        "\n━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🧾 **Atualização: 27-05-2024**\n\n"
        "**Novidades:**\n\n"
        "📖 **Comportamento aprimorado**\n"
        "   - Respostas mais precisas e naturais\n\n"
        "🚀 **Resposta de API mais rápida**\n"
        "   - Menor tempo de resposta\n\n"
        "🖼️ **Capacidade de descrever imagens**\n"
        "   - Descrições de imagens enviadas\n\n"
        "▶️ **Capacidade de resumir vídeos do YouTube**\n"
        "   - Baseado no título e descrição \n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "**Instruções:**\n\n"
        "/New - Mudar contexto da conversa\n"
        "/Help - Obter ajuda\n"
        "━━━━━━━━━━━━━━━━━━━━━━━"
    )
  
    # Criação do botão "falar com ayla"
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Falar com Ayla", callback_data="talk_to_ayla")
    keyboard.add(button)

    bot.send_message(chat_id, menu_message, reply_markup=keyboard, parse_mode="Markdown")

    # Função para lidar com callbacks dos botões
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "talk_to_ayla":
        bot.answer_callback_query(call.id)
        user_input = {
            'chat_id': call.message.chat.id,
            'message': "Olá Ayla"
        }
        result = processar_mensagem_padrao(user_input)
        bot.send_message(call.message.chat.id, result)
        
        
    #  Função para lidar com mensagens de texto
@bot.message_handler(commands=['start'])
def handle_start(message):
    send_menu_message(message.chat.id)
