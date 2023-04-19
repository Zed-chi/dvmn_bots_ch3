import logging
import random

import vk_api
from environs import Env
from telegram import Bot
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from dialogflow import Answer, detect_intent_texts
from log_config import FORMATTER, get_handler_by_env

ENV = Env()
LOGGER = logging.getLogger("VK")
LOGGER.setFormatter(FORMATTER)


def send_message_with_dialogflow_asnwer(event, vk_api):
    LOGGER.debug(f"dialogflow event {event}")
    user_id = event.message["from_id"]
    message = event.message["text"]
    answer: Answer = detect_intent_texts(
        ENV.str("GOOGLE_CLOUD_PROJECT"), user_id, message, "ru"
    )
    if answer.is_fallback:
        LOGGER.debug(f"dont understand message from user#{user_id}")
        return
    LOGGER.debug(f"sending '{answer}' to user#{user_id}")
    vk_api.messages.send(
        user_id=user_id,
        message=answer,
        random_id=random.randint(1, 1000),
    )


def listen_for_events(longpoll, api):
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            LOGGER.info("Пришло сообщение.")
            send_message_with_dialogflow_asnwer(event, api)
        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            LOGGER.debug(f"Печатает {event.obj.from_id} для {event.obj.to_id}")
        else:
            LOGGER.debug(event.type)


def run_bot():
    vk_session = vk_api.VkApi(token=ENV.str("VK_GROUP_TOKEN"))
    api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, ENV.str("VK_GROUP_ID"))

    while True:
        LOGGER.info("Bot listening for events.")
        try:
            listen_for_events(longpoll, api)
        except Exception as e:
            LOGGER.error(e)


def main():
    ENV.read_env("./.env")
    notify_tg_bot = Bot(token=ENV.str("TG_BOT_TOKEN"))
    log_handler = get_handler_by_env(notify_bot=notify_tg_bot)
    LOGGER.addHandler(log_handler)

    run_bot()


if __name__ == "__main__":
    main()
