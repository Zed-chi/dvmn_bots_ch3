import concurrent.futures as pool

from environs import Env
from telegram import Bot

from log_config import FORMATTER, get_handler_by_env
from tg_bot import LOGGER as tg_logger
from tg_bot import run_bot as tg
from vk_bot import LOGGER as vk_logger
from vk_bot import run_bot as vk

ENV = Env()


def main():
    """Main runner for bots.
    Due to one instance bot error
    we need to create bot and inject
    it to tg runner and logger(if you selected tg_logger)
    """

    ENV.read_env()
    bot = Bot(token=ENV.str("TG_BOT_TOKEN"))
    log_handler = get_handler_by_env(notify_bot=bot)

    tg_logger.addHandler(log_handler)
    vk_logger.addHandler(log_handler)

    with pool.ThreadPoolExecutor() as executor:
        executor.submit(tg, bot)
        executor.submit(vk)


if __name__ == "__main__":
    main()
