import logging
import random

import vk_api
from environs import Env
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from dialog import detect_intent_texts

env = Env()
env.read_env("./.env")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, env.str("LOG_LEVEL", "WARNING")),
)


def echo_answer(event, vk_api):
    user_id = event.message["from_id"]
    message = event.message["text"]

    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 1000),
    )


def answer_from_dialogflow(event, vk_api):
    logging.debug(f"dialogflow event {event}")
    user_id = event.message["from_id"]
    message = event.message["text"]
    answer = detect_intent_texts(env.str("PROJECT_ID"), user_id, message, "ru")
    if answer:
        vk_api.messages.send(
            user_id=user_id,
            message=answer,
            random_id=random.randint(1, 1000),
        )
    logging.debug("dialogflow message sended\n")


def main():
    vk_session = vk_api.VkApi(token=env.str("VK_GROUP_TOKEN"))
    api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, env.str("VK_GROUP_ID"))

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            logging.info("Пришло сообщение.")
            answer_from_dialogflow(event, api)
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            logging.info(
                "Новое сообщение от меня для {}, Текст:{}".format(
                    event.obj.peer_id, event.obj.text
                )
            )
        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            logging.info(f"Печатает {event.obj.from_id} для {event.obj.to_id}")
        elif event.type == VkBotEventType.GROUP_JOIN:
            logging.info(f"{event.obj.user_id} Вступил в группу!")
        elif event.type == VkBotEventType.GROUP_LEAVE:
            logging.info(f"{event.obj.user_id} Покинул группу!")
        else:
            logging.info(event.type)


if __name__ == "__main__":
    main()
