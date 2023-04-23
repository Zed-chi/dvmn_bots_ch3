import concurrent.futures as pool

from environs import Env
from telegram import Bot

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
    logger_type = env.str("LOGGER_TYPE")
    log_filepath = env.str("LOG_PATH")

    bot = Bot(token=tg_bot_token)
    log_handler = get_handler_by_env(
        logger_type, log_filepath, bot, admin_tg_chat_id
    )

    tg_logger.addHandler(log_handler)
    vk_logger.addHandler(log_handler)

    with pool.ThreadPoolExecutor() as executor:
        executor.submit(tg, bot)
        executor.submit(vk, vk_group_token, vk_group_id)


if __name__ == "__main__":
    main()
