import requests
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')

url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'


def send_telegram_message(text: str, chat_id: int):
    params = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, data=params)
    return None
