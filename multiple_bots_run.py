import logging
from threading import Thread

from environs import Env
from telegram import Bot
from telegram.utils.request import Request

from log_config import get_handler_by_env
from tg_bot import LOGGER as tg_logger
from tg_bot import run_bot as tg
from vk_bot import LOGGER as vk_logger
from vk_bot import run_bot as vk


def main():
    """Main runner for bots.
    Due to one instance bot error
    we need to create bot and inject
    it to tg runner and logger(if you selected tg_logger)
    """
    env = Env()
    env.read_env()
    tg_bot_token = env.str("TG_BOT_TOKEN")
    admin_tg_chat_id = env.str("TG_ADMIN_CHAT_ID")
    vk_group_token = env.str("VK_GROUP_TOKEN")
    vk_group_id = env.str("VK_GROUP_ID")
    google_project_name = env.str("GOOGLE_CLOUD_PROJECT")
    log_level = env.str("LOG_LEVEL")
    logger_type = env.str("LOGGER_TYPE")
    log_filepath = env.str("LOG_PATH")

    request = Request(con_pool_size=8)
    bot = Bot(token=tg_bot_token, request=request)
    log_handler = get_handler_by_env(
        logger_type, log_filepath, bot, admin_tg_chat_id
    )

    tg_logger.addHandler(log_handler)
    tg_logger.setLevel(level=getattr(logging, log_level))
    vk_logger.addHandler(log_handler)
    vk_logger.setLevel(level=getattr(logging, log_level))

    t1 = Thread(target=tg, args=[bot, google_project_name])
    t2 = Thread(
        target=vk,
        args=[vk_group_token, vk_group_id, google_project_name],
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
