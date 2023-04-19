import logging

from environs import Env
from telegram import Bot, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from dialogflow import Answer, detect_intent_texts
from log_config import get_handler_by_env, FORMATTER

ENV = Env()
LOGGER = logging.getLogger("TG")
LOGGER.setFormatter(FORMATTER)


def error_handler(update, context):
    LOGGER.error(msg="Исключение при обработке сообщения:", exc_info=context.error)


def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    LOGGER.debug(f"user#{user_id} sended start cmd")
    context.bot.send_message(chat_id=user_id, text="I'm a bot, please talk to me!")


def dialog_answer(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    LOGGER.debug(f"user#{user_id} sended message")
    answer: Answer = detect_intent_texts(
        ENV.str("GOOGLE_CLOUD_PROJECT"),
        update.effective_chat.id,
        update.message.text,
        "ru",
    )
    LOGGER.info(f"user#{user_id} sended message")
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer.text)


def run_bot(bot):
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    dialog_handler = MessageHandler(Filters.text & (~Filters.command), dialog_answer)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(dialog_handler)
    dispatcher.add_error_handler(error_handler)
    LOGGER.info("Bot listening for events.")
    updater.start_polling()


def main(bot=None):
    ENV.read_env()
    bot = Bot(token=ENV.str("TG_BOT_TOKEN"))
    log_handler = get_handler_by_env(notify_bot=bot)
    LOGGER.addHandler(log_handler)

    run_bot(bot)


if __name__ == "__main__":
    main()
