import logging

from environs import Env

ENV = Env()
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class TelegramLogsHandler(logging.Handler):
    """
    Due to one instance bot error
    we need to create common bot and inject
    it to tg runner and this handler
    """

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_handler_by_env(notify_bot=None):
    """options - FILE/TG/CONSOLE"""
    log_env = ENV.str("LOGGER")
    if log_env == "FILE":
        handler = logging.FileHandler(ENV.str("LOG_PATH"))
    elif log_env == "TG":
        if not notify_bot:
            raise ValueError("In TG Logger you need to provide a Bot instance")
        handler = TelegramLogsHandler(notify_bot, ENV.str("TG_ADMIN_CHAT_ID"))
    else:
        handler = logging.StreamHandler()
    return handler
