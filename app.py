from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from telebot.mastermind import get_response
import logging

### global objects and config
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s '
                                                '- %(levelname)s - %(message)s')

### start the flask app
app = Flask(__name__)

@app.route(f'/bot{TOKEN}', methods=['POST'])
def respond():
    # retirive json message -> to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # format the text for UTF-8 compatibility
    text = update.message.text.encode('utf-8').decode()
    print('got text message :', text)

    response = get_response(text)
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # use the bot object to link the bot to our app which lives in the URL
    s = bot.setWebhook(f'{URL}{TOKEN}')
    if s:
        return 'Webhook setup ok'
    else:
        return 'Webhook setup failed'

## homepage to make sure the engine is up
@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)
