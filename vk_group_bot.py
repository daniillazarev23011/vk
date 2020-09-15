import random
import vk_api

ACCESS_TOKEN: str = 0576310112011d739eba432d5d561c4a45d8a920b87968979303f4a256e1225f14a79d9301c2d66d51cca
GROUP_ID: int = 190673556
ADMIN_CHAT_ID: int = 257239838

vk = None  # vk session


def initialize():
    global vk
    vk = vk_api.VkApi(token=ACCESS_TOKEN)


def send_message(peer_id, text, keyboard='', photo=''):
    global vk
    vk.method('messages.send', {'peer_id': peer_id,
                                            'message': text,
                                            'keyboard': keyboard,
                                            'attachment': photo,
                                            'random_id': random.randint(0, 999999)})

