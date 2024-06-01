# main.py
from bot_instance import bot
import photo
import message
import requests
import re
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def send_menu_message(chat_id):
    menu_message = (
        "\n━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🧾 Atualização: 27-05-2024\n\n"
        "📖 Comportamento aprimorado\n\n"
        "🚀 Resposta de API está mais rápida\n\n"
        "🖼️ Capacidade de descrever imagens\n\n"
        "▶️ Capacidade de resumir vídeos do YouTube\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "instruções:\n\n"
        "/New - Mudar contexto da conversa\n"
        "/Help - Obtenção de ajuda\n"
        "━━━━━━━━━━━━━━━━━━━━━━━"
    )
  
    # Criação do botão "falar com ayla"
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Falar com Ayla", callback_data="talk_to_ayla")
    keyboard.add(button)

    bot.send_message(chat_id, menu_message, reply_markup=keyboard)

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


# Função para lidar com callbacks dos botões
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "talk_to_ayla":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Olá Ayla!")
# Variável para armazenar a última mensagem recebida do Bot2
last_bot2_message = None


# Handlers do bot
@bot.message_handler(commands=['start'])
def handle_start(message):
    menu.send_menu_message(bot, message.chat.id)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    message.processar_mensagem_padrao(bot, message)

@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):
    photo.handle_photo(bot, message)

# Inicia o botX
if __name__ == "__main__":
    bot.polling()

#Exponha a função para o Gunicorn
app = start_polling
