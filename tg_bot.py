import logging

from environs import Env
from telegram import Bot, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)
from telegram.utils.request import Request

from dialogflow import Answer, detect_intent_texts
from log_config import get_handler_by_env

LOGGER = logging.getLogger("TG")


def error_handler(update, context):
    LOGGER.error(
        msg="Исключение при обработке сообщения:",
        exc_info=context.error,
    )


def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    LOGGER.debug(f"user#{user_id} sended start cmd")
    context.bot.send_message(
        chat_id=user_id, text="I'm a bot, please talk to me!"
    )


def send_message_with_dialogflow_asnwer(
    update: Update,
    context: CallbackContext,
):
    user_id = update.effective_chat.id
    LOGGER.debug(f"user#{user_id} sended message")
    answer: Answer = detect_intent_texts(
        context.bot_data["google_project_name"],
        update.effective_chat.id,
        update.message.text,
        "ru",
    )
    LOGGER.info(f"user#{user_id} sended message")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=answer.text
    )


def run_bot(bot, google_project_name):
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher
    dispatcher.bot_data[
        "google_project_name"
    ] = google_project_name
    start_handler = CommandHandler("start", start)
    dialog_handler = MessageHandler(
        Filters.text & (~Filters.command),
        send_message_with_dialogflow_asnwer,
    )
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(dialog_handler)
    dispatcher.add_error_handler(error_handler)
    LOGGER.info("Bot listening for events.")
    updater.start_polling()


def main():
    env = Env()
    env.read_env()
    tg_bot_token = env.str("TG_BOT_TOKEN")
    admin_tg_chat_id = env.str("TG_ADMIN_CHAT_ID")
    google_project_name = env.str("GOOGLE_CLOUD_PROJECT")
    log_level = env.str("LOG_LEVEL")
    logger_type = env.str("LOGGER_TYPE")
    log_filepath = env.str("LOG_PATH")

    request = Request(con_pool_size=8)
    bot = Bot(token=tg_bot_token, request=request)
    log_handler = get_handler_by_env(
        logger_type, log_filepath, bot, admin_tg_chat_id
    )
    LOGGER.addHandler(log_handler)
    LOGGER.setLevel(level=getattr(logging, log_level))
    run_bot(bot, google_project_name)


if __name__ == "__main__":
    main()
