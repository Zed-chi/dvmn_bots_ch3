import logging
import random

import vk_api
from environs import Env
from telegram import Bot
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from dialogflow import Answer, detect_intent_texts
from log_config import get_handler_by_env

LOGGER = logging.getLogger("VK")


def send_message_with_dialogflow_asnwer(
    event, vk_api, google_project_name
):
    LOGGER.debug(f"dialogflow event {event}")
    user_id = event.message["from_id"]
    message = event.message["text"]
    answer: Answer = detect_intent_texts(
        google_project_name, user_id, message, "ru"
    )
    if answer.is_fallback:
        LOGGER.debug(
            f"dont understand message from user#{user_id}"
        )
        return
    LOGGER.debug(f"sending '{answer}' to user#{user_id}")
    vk_api.messages.send(
        user_id=user_id,
        message=answer.text,
        random_id=random.randint(1, 1000),
    )


def listen_for_events(longpoll, api, google_project_name):
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            LOGGER.info("Пришло сообщение.")
            send_message_with_dialogflow_asnwer(
                event, api, google_project_name
            )
        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            LOGGER.debug(
                f"Печатает {event.obj.from_id} для {event.obj.to_id}"
            )
        else:
            LOGGER.debug(event.type)


def run_bot(group_token, group_id, google_project_name):
    vk_session = vk_api.VkApi(token=group_token)
    api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id)
    while True:
        LOGGER.info("Bot listening for events.")
        try:
            listen_for_events(longpoll, api, google_project_name)
        except Exception as e:
            LOGGER.error(e)


def main():
    env = Env()
    env.read_env("./.env")

    tg_bot_token = env.str("TG_BOT_TOKEN")
    admin_tg_chat_id = env.str("TG_ADMIN_CHAT_ID")
    vk_group_token = env.str("VK_GROUP_TOKEN")
    vk_group_id = env.str("VK_GROUP_ID")
    log_level = env.str("LOG_LEVEL")
    logger_type = env.str("LOGGER_TYPE")
    log_filepath = env.str("LOG_PATH")
    google_project_name = env.str("GOOGLE_CLOUD_PROJECT")

    notify_tg_bot = Bot(token=tg_bot_token)
    log_handler = get_handler_by_env(
        logger_type,
        log_filepath,
        notify_tg_bot,
        admin_tg_chat_id,
    )
    LOGGER.addHandler(log_handler)
    LOGGER.setLevel(level=getattr(logging, log_level))
    run_bot(vk_group_token, vk_group_id, google_project_name)


if __name__ == "__main__":
    main()
