from flask import Flask
import telegram
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def send_horoscope():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    user_id = os.environ.get("TELEGRAM_USER_ID")
    bot = telegram.Bot(token=bot_token)
    RASHI_NAME = 'ವೃಷಭ'

    url = 'https://m.dailyhunt.in/news/india/kannada/ganesha+speaks+kannada@GaneshaSpeaksKannada'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_divs = soup.find_all('div', class_='details')
    horoscope_text = "ಇಂದು ನಿಮ್ಮ ಭವಿಷ್ಯವಾಣಿ ಲಭ್ಯವಿಲ್ಲ."

    for block in all_divs:
        if block.find('h2') and 'ವೃಷಭ' in block.find('h2').text:
            p = block.find('p')
            if p:
                horoscope_text = p.text.strip()
            break

    today_str = datetime.now().strftime('%d-%m-%Y')
    message = f"*ದೈನಂದಿನ ರಾಶಿಫಲ – ವೃಷಭ*\n🗓 {today_str}\n\n{horoscope_text}"
    bot.send_message(chat_id=user_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
    return "Horoscope sent!"
