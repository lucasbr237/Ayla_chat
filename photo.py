from gradio_client import Client, file
from bot_instance import bot
import response
import requests
import re
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from msg2 import processar_mensagem_padrao
import os

# Função para garantir que cada usuário tenha sua própria subpasta de fotos
def ensure_user_photo_folder(user_id):
    folder_path = f"conversations/{user_id}/photos"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Função para salvar a foto do usuário com nome único
def save_photo(user_id, photo_data):
    folder_path = ensure_user_photo_folder(user_id)
    num_photos = len(os.listdir(folder_path))
    photo_path = f"{folder_path}/photo_{num_photos + 1}.jpg"
    with open(photo_path, "wb") as file:
        file.write(photo_data)

# Função para obter a lista de fotos do usuário
def get_user_photos(user_id):
    folder_path = ensure_user_photo_folder(user_id)
    return [f"{folder_path}/{filename}" for filename in os.listdir(folder_path)]

# Função para lidar com mensagens de foto
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        # Salvar a foto mais recente na pasta do usuário
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        user_id = message.chat.id
        save_photo(user_id, downloaded_file)
        
        # Processar a foto mais recente
        photo_path = get_latest_photo_path(user_id)
        response = query(photo_path)
        caption = response.json()[0]['generated_text']
        translated_caption = translate_text(caption, 'en', 'pt')
        
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

# Função para obter o caminho da foto mais recente do usuário
def get_latest_photo_path(user_id):
    folder_path = ensure_user_photo_folder(user_id)
    photo_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
    if photo_files:
        latest_photo = sorted(photo_files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)), reverse=True)[0]
        return os.path.join(folder_path, latest_photo)
    else:
        return None

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
