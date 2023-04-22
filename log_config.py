import logging

from environs import Env

ENV = Env()
FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class TelegramLogsHandler(logging.Handler):
    """TG Logger
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
        self.tg_bot.send_message(
            chat_id=self.chat_id, text=log_entry
        )


def get_handler_by_env(
    env_value, log_filepath, notify_bot, admin_chat_id
):
    """Handler logger getter.
    Options:
    - FILE
    - TG
    - CONSOLE
    """
    if env_value == "FILE":
        handler = logging.FileHandler(log_filepath)
    elif env_value == "TG":
        handler = TelegramLogsHandler(notify_bot, admin_chat_id)
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(FORMATTER)
    return handler
