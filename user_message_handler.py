from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from collections import defaultdict
import vk_group_bot
from user import UserCondition, User
import bot
import res

bot_methods = defaultdict(dict)


def bot_method(condition: int, name: str):
    def decorator(method):
        global bot_methods
        bot_methods[condition][name] = method
        return method

    return decorator


bot_inputs = {}


def bot_input(condition: int):
    def decorator(method):
        global bot_inputs
        bot_inputs[condition] = method
        return method

    return decorator


# KEYBOARDS
begin_keyboard = VkKeyboard(one_time=False)
begin_keyboard.add_button("Начать", VkKeyboardColor.PRIMARY)
begin_keyboard = begin_keyboard.get_keyboard()

settings_keyboard = VkKeyboard(one_time=False)
settings_keyboard.add_button("Имя", VkKeyboardColor.DEFAULT)
settings_keyboard.add_button("Возраст", VkKeyboardColor.DEFAULT)
settings_keyboard.add_line()
settings_keyboard.add_button("О себе", VkKeyboardColor.DEFAULT)
settings_keyboard.add_button("Фото", VkKeyboardColor.DEFAULT)
settings_keyboard.add_line()
settings_keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
settings_keyboard = settings_keyboard.get_keyboard()

input_cancel_keyboard = VkKeyboard(one_time=False)
input_cancel_keyboard.add_button("Отмена", VkKeyboardColor.DEFAULT)
input_cancel_keyboard = input_cancel_keyboard.get_keyboard()

main_menu_keyboard = VkKeyboard(one_time=False)
main_menu_keyboard.add_button(res.emoji['search'], VkKeyboardColor.PRIMARY)
main_menu_keyboard.add_button(res.emoji['fax'], VkKeyboardColor.PRIMARY)
main_menu_keyboard.add_button(res.emoji['settings'], VkKeyboardColor.DEFAULT)
main_menu_keyboard = main_menu_keyboard.get_keyboard()

searching_partner_keyboard = VkKeyboard(one_time=False)
searching_partner_keyboard.add_button(res.emoji['like'], VkKeyboardColor.POSITIVE)
searching_partner_keyboard.add_button(res.emoji['dislike'], VkKeyboardColor.NEGATIVE)
searching_partner_keyboard.add_button(res.emoji['report'], VkKeyboardColor.DEFAULT)
searching_partner_keyboard.add_button(res.emoji['back'], VkKeyboardColor.PRIMARY)
searching_partner_keyboard = searching_partner_keyboard.get_keyboard()

chat_keyboard = VkKeyboard(one_time=False)
chat_keyboard.add_button(res.emoji['search'], VkKeyboardColor.NEGATIVE)
chat_keyboard.add_button(res.emoji['report'], VkKeyboardColor.DEFAULT)
chat_keyboard.add_button(res.emoji['back'], VkKeyboardColor.PRIMARY)
chat_keyboard = chat_keyboard.get_keyboard()


def handle(message):
    user_id: int = message.peer_id
    text: str = message.text
    # add attachment to text
    if len(message.attachments) == 1:
        if message.attachments[0]['type'] == 'photo':
            text += f" photo{message.attachments[0]['photo']['owner_id']}" \
                    f"_{message.attachments[0]['photo']['id']}" \
                    f"_{message.attachments[0]['photo'].get('access_key', '')}"
    text = text.strip()
    if text == '':
        text = "Empty message"

    user = bot.get_user_by_id(user_id)

    global bot_methods
    if user.condition in bot_inputs:
        bot_inputs[user.condition](user, text)
    elif text in bot_methods[user.condition]:
        bot_methods[user.condition][text](user)
    else:
        bot_methods[user.condition]["Гайд"](user)


@bot_method(UserCondition.BEGIN, "Начать")
def begin(user: User):
    user.condition = UserCondition.SETTINGS
    vk_group_bot.send_message(user.id, "Добро пожаловать, кексик!\n"
                                       "Для начала зарегистрируем тебя!\n"
                                       "Вот меню настроек.", settings_keyboard)


@bot_method(UserCondition.BEGIN, "Гайд")
def begin_guide(user: User):
    vk_group_bot.send_message(user.id, "Добро пожаловать, кексик!\n"
                                       "Ты у нас впервые?\n"
                                       "Нажми \"начать\", чтобы продолжить.", begin_keyboard)


@bot_method(UserCondition.MAIN_MENU, res.emoji['settings'])
def settings(user: User):
    user.condition = UserCondition.SETTINGS
    vk_group_bot.send_message(user.id, f'ТВОЙ АККАУНТ\n\n'
                                       f'ID: {user.id}\n'
                                       f'{user.name}, {user.age}:\n'
                                       f'\"{user.info}\"',
                              settings_keyboard, photo=user.photo)


@bot_method(UserCondition.SETTINGS, "Гайд")
def settings_guide(user: User):
    vk_group_bot.send_message(user.id, "Вы находитесь в меню настроек.\n"
                                       "Доступные команды:\n"
                                       "- Имя (Указать свое имя)\n"
                                       "- Возраст (Указать возраст)\n"
                                       "- О себе (Добавить доп. информацию в анкету)\n"
                                       "- Фото (Прислать фото профиля)\n"
                                       "- Завершить (Если заполнены все поля выше, "
                                       "закончить редактирование аккаунта)", settings_keyboard)


@bot_method(UserCondition.SETTINGS, "Имя")
def settings_name(user: User):
    user.condition = UserCondition.SETTINGS_NAME
    vk_group_bot.send_message(user.id, "Как же вас зовут?",
                              input_cancel_keyboard)


@bot_input(UserCondition.SETTINGS_NAME)
def input_settings_name(user: User, data: str):
    if data == "Отмена":
        user.condition = UserCondition.SETTINGS
        vk_group_bot.send_message(user.id, "Вернул тебя назад", settings_keyboard)
    else:
        user.name = data
        user.condition = UserCondition.SETTINGS
        vk_group_bot.send_message(user.id, "Приятно познакомиться!!", settings_keyboard)


@bot_method(UserCondition.SETTINGS, "Возраст")
def settings_age(user: User):
    user.condition = UserCondition.SETTINGS_AGE
    vk_group_bot.send_message(user.id, "Сколько вам полных лет? Чур не обманывать, знаем мы таких!",
                              input_cancel_keyboard)


@bot_input(UserCondition.SETTINGS_AGE)
def input_settings_age(user: User, data: str):
    if data == "Отмена":
        user.condition = UserCondition.SETTINGS
        vk_group_bot.send_message(user.id, "Вернул тебя назад", settings_keyboard)
    else:
        try:
            user.age = int(data)
            if user.age > 120 or user.age < 1:
                raise ValueError
            user.condition = UserCondition.SETTINGS
            vk_group_bot.send_message(user.id, "Самое время искать тяночку!\n"
                                               "В вашем возрасте без этого никак!", settings_keyboard)
        except ValueError:
            vk_group_bot.send_message(user.id, "Неверный возраст", input_cancel_keyboard)


@bot_method(UserCondition.SETTINGS, "О себе")
def settings_info(user: User):
    user.condition = UserCondition.SETTINGS_INFO
    vk_group_bot.send_message(user.id, "А расскажи-ка о себе поподробней! Мне очень интересно, правда...",
                              input_cancel_keyboard)


@bot_input(UserCondition.SETTINGS_INFO)
def input_settings_info(user: User, data: str):
    if data == "Отмена":
        user.condition = UserCondition.SETTINGS
        vk_group_bot.send_message(user.id, "Вернул тебя назад", settings_keyboard)
    else:
        user.info = data
        user.condition = UserCondition.SETTINGS
        vk_group_bot.send_message(user.id, "А я сразу, как ты написал, понял, что ты лютый поц!",
                                  settings_keyboard)


@bot_method(UserCondition.SETTINGS, "Фото")
def settings_photo(user: User):
    user.condition = UserCondition.SETTINGS_PHOTO
    vk_group_bot.send_message(user.id, "Все обязательно должны увидеть твое фото!\n"
                                       "Уверен, что ты супер-красавчик.\n"
                                       "Пришли изображение пожалуйста!!\n"
                                       "(Фото должно быть из открытого источника сайта ВК,\n"
                                       "Пересылать с помощью кнопки \"ПОДЕЛИТЬСЯ\", спасибо!)",
                              input_cancel_keyboard)


@bot_input(UserCondition.SETTINGS_PHOTO)
def input_settings_photo(user: User, data: str):
    if data == "Отмена":
        user.condition = UserCondition.SETTINGS
        vk_group_bot.send_message(user.id, "Вернул тебя назад", settings_keyboard)
    else:
        user.photo = data
        user.condition = UserCondition.SETTINGS
        vk_group_bot.send_message(user.id, "Ты о-о-очень к-к-красивая а ты занята ладно все пока",
                                  settings_keyboard)


@bot_method(UserCondition.SETTINGS, "Завершить")
def settings_end(user: User):
    if user.name and user.age and user.info and user.photo:
        if bot.register_user(user):
            user.condition = UserCondition.MAIN_MENU
            vk_group_bot.send_message(user.id, 'Принято!')
            vk_group_bot.send_message(user.id,
                                      f'ТВОИ ДАННЫЕ:\n\n'
                                      f'ID: {user.id}\n'
                                      f'{user.get_profile_info()}',
                                      main_menu_keyboard, user.photo)
    else:
        vk_group_bot.send_message(user.id, 'Не все поля заполнены!', settings_keyboard)


@bot_method(UserCondition.MAIN_MENU, "Гайд")
def main_menu_guide(user: User):
    vk_group_bot.send_message(user.id, "Вы находитесь в главном меню.\n"
                                       "Доступные функции:\n"
                                       "- Поиск (Начать искать тяночку)\n"
                                       "- Почта (не готово)\n"
                                       "- Настройки (Изменить данные аккаунта)\n",
                              main_menu_keyboard)


@bot_method(UserCondition.SEARCHING_PARTNER, "Гайд")
def searching_partner_guide(user: User):
    vk_group_bot.send_message(user.id, "Вы в режиме поиска лубви!\n"
                                       "Доступные функции:\n"
                                       "- Оаоамм (Влюбился - в случае взаимности,"
                                       " вам обоим будет прислана ссылка на друг друга)\n"
                                       "- Неее (Получить следующего человека)\n"
                                       "- Репорт (Пожаловаться на пользователя)\n"
                                       "- Меню (Вернуться в главное меню)\n",
                              searching_partner_keyboard)


def next_partner(user: User):
    is_partner_fan = True
    partner = bot.get_fan_of(user)
    if partner is None:
        is_partner_fan = False
        partner = bot.get_random_partner(user)

    if partner is not None:
        user.set_proposed_partner(partner, is_partner_fan)
        vk_group_bot.send_message(user.id,
                                  f"Ты только посмотри, какая женщина!\n\n"
                                  f"{partner.get_profile_info()}",
                                  searching_partner_keyboard, partner.photo)
    else:
        vk_group_bot.send_message(user.id, "Ошибочка", searching_partner_keyboard)


@bot_method(UserCondition.MAIN_MENU, res.emoji['search'])
def searching_partner(user: User):
    user.condition = UserCondition.SEARCHING_PARTNER
    # get first partner
    next_partner(user)


@bot_method(UserCondition.SEARCHING_PARTNER, res.emoji['like'])
def like_partner(user: User):
    if user.proposed_partner is not None:
        if user.proposed_partner_is_fan:
            vk_group_bot.send_message(user.id,
                                      f"Тили-тили тесто!! Поздравляю, боец!\n"
                                      f"Ваша лубов:\n\n"
                                      f"{user.proposed_partner.get_profile_info()}"
                                      f"Только не ссы\n"
                                      f"vk.com/id{user.proposed_partner.id}",
                                      user.proposed_partner.photo)
            vk_group_bot.send_message(user.proposed_partner.id,
                                      f"Тили-тили тесто!! Поздравляю, боец!\n"
                                      f"Ваша лубов:\n\n"
                                      f"{user.get_profile_info()}"  
                                      f"Только не ссы\n"
                                      f"vk.com/id{user.id}",
                                      user.photo)
            user.set_proposed_partner(None, None)
        else:
            user.proposed_partner.expand_update_fanbase(user.id)
    next_partner(user)


@bot_method(UserCondition.SEARCHING_PARTNER, res.emoji['dislike'])
def skip_partner(user: User):
    user.set_proposed_partner(None, None)
    next_partner(user)


def report(sender: User, user: User):
    vk_group_bot.send_message(vk_group_bot.ADMIN_CHAT_ID,
                              f"Report to the user id{user.id}:\n"
                              f"{user.get_profile_info()}",
                              photo=user.photo)
    vk_group_bot.send_message(sender.id, "Жалоба отправлена админу, спасибо! :*")


@bot_method(UserCondition.SEARCHING_PARTNER, res.emoji['report'])
def report_partner(user: User):
    report(user, user.proposed_partner)
    user.set_proposed_partner(None, None)
    next_partner(user)


@bot_method(UserCondition.SEARCHING_PARTNER, res.emoji['back'])
def exit_searching_partner(user: User):
    user.set_proposed_partner(None, None)
    user.condition = UserCondition.MAIN_MENU
    vk_group_bot.send_message(user.id, "Ну и правильно, без баб!", main_menu_keyboard)


@bot_method(UserCondition.SEARCHING_CHAT, "Гайд")
def searching_chat_guide(user: User):
    vk_group_bot.send_message(user.id, "Вы в чате!\n"
                                       "Доступные функции:\n"
                                       "- Поиск (Искать собеседника)\n"
                                       "- Репорт (Пожаловаться на пользователя)\n"
                                       "- Меню (Вернуться в главное меню)\n",
                              chat_keyboard)


@bot_method(UserCondition.MAIN_MENU, res.emoji['fax'])
def searching_chat(user: User):
    user.condition = UserCondition.SEARCHING_CHAT
    vk_group_bot.send_message(user.id, "Добро пожаловать в чат!\n"
                                       "Нажмите \"Поиск\", чтобы найти собеседника",
                              chat_keyboard)


@bot_method(UserCondition.SEARCHING_CHAT, res.emoji['search'])
def find_chat(user: User):
    partner = bot.get_chat(user)
    if partner is None:
        vk_group_bot.send_message(user.id,
                                  "Вы в очереди, подождите...",
                                  chat_keyboard)
    else:
        user.proposed_partner = partner
        partner.proposed_partner = user

        user.condition = UserCondition.CHATTING
        vk_group_bot.send_message(user.id,
                                  f"Найден собеседник:\n\n"
                                  f"{partner.get_profile_info()}\n\n"
                                  f"Общайтесь!",
                                  chat_keyboard, photo=partner.photo)

        partner.condition = UserCondition.CHATTING
        vk_group_bot.send_message(partner.id,
                                  f"Найден собеседник:\n\n"
                                  f"{user.get_profile_info()}\n\n"
                                  f"Общайтесь!",
                                  chat_keyboard, photo=user.photo)


def end_chat(user: User):
    vk_group_bot.send_message(user.proposed_partner.id,
                              "Беседа завершена, хорошо побалакали :*",
                              chat_keyboard)
    user.proposed_partner.condition = UserCondition.SEARCHING_CHAT
    user.proposed_partner.proposed_partner = None

    vk_group_bot.send_message(user.id,
                              "Беседа завершена :(",
                              chat_keyboard)
    user.condition = UserCondition.SEARCHING_CHAT
    user.proposed_partner = None


@bot_method(UserCondition.SEARCHING_CHAT, res.emoji['back'])
def exit_searching_chat(user: User):
    bot.searching_chat_users.pop(user)
    user.condition = UserCondition.MAIN_MENU
    vk_group_bot.send_message(user.id,
                              "Сколько можно уже болтать!",
                              main_menu_keyboard)


@bot_input(UserCondition.CHATTING)
def chatting(user: User, data: str):
    if data == res.emoji['search']:
        end_chat(user)
        find_chat(user)
    elif data == res.emoji['report']:
        report(user, user.proposed_partner)
        end_chat(user)
    elif data == res.emoji['back']:
        end_chat(user)
        exit_searching_chat(user)
    else:
        vk_group_bot.send_message(user.proposed_partner.id, data, chat_keyboard)
