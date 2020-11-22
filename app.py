import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from dialog import detect_intent_texts

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


updater = Updater(token=os.getenv("token"))
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    text = update.message.text
    answer = detect_intent_texts(os.getenv("dialog_id"), "test", text, "ru")
    print(answer)
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
start_handler = CommandHandler('start', start)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
updater.start_polling()