import random

import vk_api
from environs import Env
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from dialogflow import detect_intent_texts
from log_config import get_logger, select_handler_by_env

env = Env()
env.read_env("./.env")

LOGGER = get_logger("VK")
select_handler_by_env(LOGGER)


def echo_answer(event, vk_api):
    user_id = event.message["from_id"]
    message = event.message["text"]

    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 1000),
    )


def answer_from_dialogflow(event, vk_api):
    LOGGER.debug(f"dialogflow event {event}")
    user_id = event.message["from_id"]
    message = event.message["text"]
    answer = detect_intent_texts(
        env.str("GOOGLE_CLOUD_PROJECT"), user_id, message, "ru"
    )
    if answer:
        LOGGER.debug(f"sending '{answer}' to user#{user_id}")
        vk_api.messages.send(
            user_id=user_id,
            message=answer,
            random_id=random.randint(1, 1000),
        )
    else:
        LOGGER.debug(f"dont understand message from user#{user_id}")
    LOGGER.debug("dialogflow message sended\n")


def listening_cycle(longpoll, api):
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            LOGGER.info("Пришло сообщение.")
            answer_from_dialogflow(event, api)
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            LOGGER.info(
                "Новое сообщение от меня для {}, Текст:{}".format(
                    event.obj.peer_id, event.obj.text
                )
            )
        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            LOGGER.info(f"Печатает {event.obj.from_id} для {event.obj.to_id}")
        elif event.type == VkBotEventType.GROUP_JOIN:
            LOGGER.info(f"{event.obj.user_id} Вступил в группу!")
        elif event.type == VkBotEventType.GROUP_LEAVE:
            LOGGER.info(f"{event.obj.user_id} Покинул группу!")
        else:
            LOGGER.info(event.type)


def main():
    vk_session = vk_api.VkApi(token=env.str("VK_GROUP_TOKEN"))
    api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, env.str("VK_GROUP_ID"))

    while True:
        LOGGER.info("listening starts...")
        try:
            listening_cycle(longpoll, api)
        except Exception as e:
            LOGGER.error(e)


if __name__ == "__main__":
    main()
