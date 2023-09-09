from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
from database import functions as database_functions


bot = AsyncTeleBot(f'{config.token}')
users = config.users


def make_markup_and_text(message, requests_new, requests_in_processing, requests_accepted, requests_declined):

    if message.chat.id in users:
        markup_inline = types.InlineKeyboardMarkup()
        markup_inline.add(types.InlineKeyboardButton(f'🔔 Новые заявки ({len(requests_new)})',
                                                    callback_data='Requests_new|0'))
        markup_inline.add(types.InlineKeyboardButton(f'📝 Заявки в обработке ({len(requests_in_processing)})',
                                                    callback_data='Requests_in_processing|0'))
        markup_inline.add(types.InlineKeyboardButton(f'👨‍💻 Заявки в работе ({len(requests_accepted)})',
                                                    callback_data='Requests_accepted|0'))
        markup_inline.add(types.InlineKeyboardButton(f'🗑 Корзина заявок ({len(requests_declined)})',
                                                    callback_data='Requests_declined|0'))
        markup_inline.add(types.InlineKeyboardButton(f'🌀 Обновить страницу', callback_data='Main'))
        message_text = '📩 Список полученных заявок 📩'

    else:
        markup_inline = None
        message_text = '🤗 Извините, кажется у вас нет доступа к боту, получите ваш id с помощью ' \
                        '/recipient и попросите администратора проекта добавить вас в список ' \
                        'пользователей'

    return markup_inline, message_text

async def send(message):

    database_functions.first_connect_from_user()
    requests_new = database_functions.get_requests_new()
    requests_in_processing = database_functions.get_requests_in_processing()
    requests_accepted = database_functions.get_requests_accepted()
    requests_declined = database_functions.get_requests_declined()

    markup_inline, message_text = make_markup_and_text(message, requests_new, requests_in_processing, 
                                               requests_accepted, requests_declined)

    await bot.send_message(message.chat.id, text=message_text, reply_markup=markup_inline)

async def edit(message):

    database_functions.first_connect_from_user()
    requests_new = database_functions.get_requests_new()
    requests_in_processing = database_functions.get_requests_in_processing()
    requests_accepted = database_functions.get_requests_accepted()
    requests_declined = database_functions.get_requests_declined()

    markup_inline, message_text = make_markup_and_text(message, requests_new, requests_in_processing, 
                                         requests_accepted, requests_declined)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text)
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup_inline)