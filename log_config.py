import logging

from environs import Env
from telegram import Bot

env = Env()

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, env.str("LOG_LEVEL", "WARNING")))
    return logger


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def select_handler_by_env(logger: logging.Logger, bot=None):
    """options - FILE/TG/CONSOLE"""
    log_env = env.str("LOGGER")
    if log_env == "FILE":
        handler = logging.FileHandler(env.str("LOG_PATH"))

    elif log_env == "TG":
        if bot is None:
            bot = Bot(token=env.str("TG_BOT_TOKEN"))
        handler = TelegramLogsHandler(bot, env.str("TG_ADMIN_CHAT_ID"))
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(FORMATTER)
    logger.addHandler(handler)
