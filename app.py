from bot_instance import bot
import photo
import requests
import re
import time
import telebot
import os
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from msg2 import processar_mensagem_padrao


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


bot.polling()


# Exponha a função para o Gunicorn
app = handle_message
