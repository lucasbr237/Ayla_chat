from bot_instance import bot
import message
import requests
import re
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from message import processar_mensagem_padrao

# Função para lidar com mensagens de foto
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global last_bot2_message
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = "/storage/emulated/0/photo.jpg"
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        response = query(file_path)
        caption = response.json()[0]['generated_text']
        translated_caption = translate_text(caption, 'en', 'pt')
        last_bot2_message = translated_caption
        # Chama a função para processar a mensagem e envia a legenda traduzida como entrada
        user_input = {
            'chat_id': message.chat.id,
            'message': translated_caption
        }
        result = processar_mensagem_padrao(user_input)
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, "Desculpe, ocorreu um erro ao processar a sua foto.")
        print(f"Erro ao processar a foto: {e}")

def query(filename):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": "Bearer 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"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response

def translate_text(text, source_lang, target_lang):
    params = {
        'q': text,
        'langpair': f'{source_lang}|{target_lang}'
    }
    response = requests.get('https://api.mymemory.translated.net/get', params=params)
    translated_text = response.json()['responseData']['translatedText']
    return translated_text
