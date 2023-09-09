from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
from database import functions as database_functions
from modules import functions as subsidiary_functions


bot = AsyncTeleBot(f'{config.token}')


def make_markup(request_id, status):

    call_keyword = subsidiary_functions.get_call_keyword_from_status(status)

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton('🛠 Изменить статус заявки',
                                                    callback_data=f'Change_status|{request_id}'))
    markup_inline.add(types.InlineKeyboardButton('🔙 Назад', callback_data=f'{call_keyword}|0'))

    return markup_inline



async def edit(message, request_id):

    request = database_functions.get_request_by_id(request_id)
    name, tnumber, description, status = request[0][1], request[0][2], request[0][3], request[0][4]

    status_in_text = subsidiary_functions.get_text_from_status(status)
    message_text = f'👨‍💼 Имя: {name}\n📱 Номер телефона: {tnumber}\n' + \
                    f'📋 Описание: {description}\n🖇 Статус: {status_in_text}'
    
    markup_inline = make_markup(request_id, status)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                text=f'Заявка №{request_id}\n{message_text}')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                        reply_markup=markup_inline)