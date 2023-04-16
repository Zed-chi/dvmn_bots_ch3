import logging

from environs import Env
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
from dialog import detect_intent_texts

env = Env()
env.read_env()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def reply_same_text(update: Update, context: CallbackContext):
    pass


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def dialog_answer(update: Update, context: CallbackContext):
    res = detect_intent_texts(
        env.str("PROJECT_ID"), update.effective_chat.id, [update.message.text], "ru"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)


def main():
    updater = Updater(token=env.str("TG_TOKEN"))
    dispatcher = updater.dispatcher
    # stuff
    start_handler = CommandHandler("start", start)
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dialog_handler = MessageHandler(Filters.text & (~Filters.command), dialog_answer)

    dispatcher.add_handler(start_handler)
    # dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(dialog_handler)

    updater.start_polling()


if __name__ == "__main__":
    main()
