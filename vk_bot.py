import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from environs import Env


env = Env()
env.read_env("./.env")


vk_session = vk_api.VkApi(token=env.str("VK_GROUP_TOKEN"))
longpoll = VkBotLongPoll(vk_session, env.str("VK_GROUP_ID"))

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        print("Новое сообщение:")
        if event.to_me:
            print("Для меня от: ", event.user_id)
        else:
            print("От меня для: ", event.user_id)
        print("Текст:", event.text)
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
