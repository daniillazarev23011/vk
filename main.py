from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_group_bot
import database
import bot
import user_message_handler
import admin_message_handler


if __name__ == "__main__":
    vk_group_bot.initialize()
    database.open()
    bot.initialize()

    longpool = VkBotLongPoll(vk_group_bot.vk, vk_group_bot.GROUP_ID)
    Running = True
    while Running:
        for event in longpool.listen():
            if not Running:
                break

            # handle events
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.peer_id != vk_group_bot.ADMIN_CHAT_ID:
                    user_message_handler.handle(event.object)
                else:
                    admin_message_handler.handle(event.object)
