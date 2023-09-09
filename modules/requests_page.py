from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
from database import functions as database_functions
from modules import functions as subsidiary_functions


bot = AsyncTeleBot(f'{config.token}')


def make_markup(requests, page_id, status):

    call_keyword = subsidiary_functions.get_call_keyword_from_status(status)
    emoji_for_list = subsidiary_functions.get_emoji_from_status(status)

    markup_inline = types.InlineKeyboardMarkup()

    if len(requests) < page_id + 10:
        last_post_counter = len(requests)
    else:
        last_post_counter = page_id + 10

    for i in range(page_id, last_post_counter):
        markup_inline.add(types.InlineKeyboardButton(f'{emoji_for_list} Заявка №{requests[i][0]}',
                                                        callback_data=f'Request_info|{requests[i][0]}'))
    if (page_id != 0) and (page_id + 10 < len(requests)):
        markup_inline.add(types.InlineKeyboardButton('⬅️ Предыдущая страница',
                                                        callback_data=f'{call_keyword}|{page_id - 10}'),
                            types.InlineKeyboardButton('Следующая страница ➡️',
                                                        callback_data=f'{call_keyword}|{page_id + 10}')
                            )
    elif page_id != 0:
        markup_inline.add(types.InlineKeyboardButton('⬅️ Предыдущая страница',
                                                        callback_data=f'{call_keyword}|{page_id - 10}'))
    elif page_id + 10 < len(requests):
        markup_inline.add(types.InlineKeyboardButton('Следующая страница ➡️',
                                                        callback_data=f'{call_keyword}|{page_id + 10}'))
    markup_inline.add(types.InlineKeyboardButton('🔙 Назад', callback_data='Main'))

    return markup_inline


async def edit(message, page_id, status):
    
    match status:
        case 'new':
            requests = database_functions.get_requests_new()
        case 'in_processing':
            requests = database_functions.get_requests_in_processing()
        case 'accepted':
            requests = database_functions.get_requests_accepted()
        case 'declined':
            requests = database_functions.get_requests_declined()

    markup_inline = make_markup(requests, page_id, status)
    message_caption = subsidiary_functions.get_caption_from_status(status)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                text=f'{message_caption} ({page_id}-{page_id + 10})')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                        reply_markup=markup_inline)
    

async def send(message, page_id, status):

    match status:
        case 'new':
            requests = database_functions.get_requests_new()
        case 'in_processing':
            requests = database_functions.get_requests_in_processing()
        case 'accepted':
            requests = database_functions.get_requests_accepted()
        case 'declined':
            requests = database_functions.get_requests_declined()

    markup_inline = make_markup(requests, page_id, status)
    message_caption = subsidiary_functions.get_caption_from_status(status)

    await bot.send_message(chat_id=message.chat.id, text=f'{message_caption} ({page_id}-{page_id + 10})',
                           reply_markup=markup_inline)