from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
from database import functions as database_functions

bot = AsyncTeleBot(f'{config.token}')

def make_markup(request_id, from_status):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    markup_inline.add(types.InlineKeyboardButton('🔔 Новая заявка',
                                                callback_data=f'Changing_status|{request_id}|new|{from_status}'))
    markup_inline.add(types.InlineKeyboardButton(
                        '📝 Заявка в обработке', callback_data=f'Changing_status|{request_id}|in_processing|{from_status}'))
    markup_inline.add(types.InlineKeyboardButton('👨‍💻 Заявка в работе',
                                                callback_data=f'Changing_status|{request_id}|accepted|{from_status}'))
    markup_inline.add(types.InlineKeyboardButton('🗑 Заявка отклонена',
                                                callback_data=f'Changing_status|{request_id}|declined|{from_status}'))
    return markup_inline

async def edit(message, request_id):

    request = database_functions.get_request_by_id(request_id)
    from_status = request[0][4]

    markup_inline = make_markup(request_id, from_status)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='🛠 Выберите новый статус заявки')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup_inline)