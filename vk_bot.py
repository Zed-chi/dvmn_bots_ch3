import random

import vk_api
from environs import Env
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from dialog import detect_intent_texts

env = Env()
env.read_env("./.env")


def echo_answer(event, vk_api):
    print(f"event.message = {event.message}")
    user_id = event.message["from_id"]
    message = event.message["text"]

    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 1000),
    )


def answer_from_dialogflow(event, vk_api):
    user_id = event.message["from_id"]
    message = event.message["text"]
    answer = detect_intent_texts(env.str("PROJECT_ID"), user_id, message, "ru")
    vk_api.messages.send(
        user_id=user_id,
        message=answer,
        random_id=random.randint(1, 1000),
    )


def main():
    vk_session = vk_api.VkApi(token=env.str("VK_GROUP_TOKEN"))
    api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, env.str("VK_GROUP_ID"))

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print("Новое сообщение:")
            answer_from_dialogflow(event, api)
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            print("Новое сообщение:")
            print("От меня для: ", end="")
            print(event.obj.peer_id)
            print("Текст:", event.obj.text)
            print()
        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            print("Печатает ", end="")
            print(event.obj.from_id, end=" ")
            print("для ", end="")
            print(event.obj.to_id)
            print()
        elif event.type == VkBotEventType.GROUP_JOIN:
            print(event.obj.user_id, end=" ")
            print("Вступил в группу!")
            print()
        elif event.type == VkBotEventType.GROUP_LEAVE:
            print(event.obj.user_id, end=" ")
            print("Покинул группу!")
            print()
        else:
            print(event.type)
            print()


if __name__ == "__main__":
    main()
