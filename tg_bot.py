from environs import Env
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from dialogflow import detect_intent_texts
from log_config import get_logger, select_handler_by_env

env = Env()
env.read_env()
LOGGER = get_logger("TG")


def error_handler(update, context):
    LOGGER.error(msg="Исключение при обработке сообщения:", exc_info=context.error)
    """
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    message = f"{tb_string}"
    context.bot.send_message(chat_id=env.str("ADMIN_ID"), text=message)
    """


def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    LOGGER.debug(f"user#{user_id} sended start cmd")
    context.bot.send_message(chat_id=user_id, text="I'm a bot, please talk to me!")


def dialog_answer(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    LOGGER.debug(f"user#{user_id} sended message")
    answer = detect_intent_texts(
        env.str("GOOGLE_CLOUD_PROJECT"),
        update.effective_chat.id,
        update.message.text,
        "ru",
    )
    if answer:
        LOGGER.info(f"user#{user_id} sended message")
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    else:
        LOGGER.debug(f"dont understand message from user#{user_id}")


def main(bot=None):
    if bot:
        LOGGER.debug("external bot inject")
        updater = Updater(bot=bot)
    else:
        updater = Updater(token=env.str("TG_BOT_TOKEN"))
    select_handler_by_env(LOGGER, bot=updater.bot)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dialog_handler = MessageHandler(Filters.text & (~Filters.command), dialog_answer)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(dialog_handler)
    dispatcher.add_error_handler(error_handler)

    LOGGER.info("Bot listening for events.")
    updater.start_polling()


if __name__ == "__main__":
    main()
