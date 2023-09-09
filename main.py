from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from modules import start, requests_page, request_info, change_status
from database import functions as database_functions
import modules.functions as subsidiary_functions


bot = AsyncTeleBot(f'{config.token}')


@bot.message_handler(commands=['recipient'])
async def recipient(message):
    await bot.send_message(message.chat.id, f'Ваш recipient-id: {message.chat.id}')


@bot.message_handler(commands=['start'])
async def main(message):
    await start.send(message)


@bot.callback_query_handler(func=lambda call: True)
async def callback(call):
    
    calling_data = call.data.split('|')

    match calling_data[0]:
        case 'Main':
            await start.edit(call.message)
        case 'Refresh_main':
            await subsidiary_functions.delete_message(call.message)
            await start.send(call.message)
        case 'Requests_new':
            await requests_page.edit(message=call.message, page_id=int(calling_data[1]), status='new')
        case 'Requests_in_processing':
            await requests_page.edit(message=call.message, page_id=int(calling_data[1]), status='in_processing')
        case 'Requests_accepted':
            await requests_page.edit(message=call.message, page_id=int(calling_data[1]), status='accepted')
        case 'Requests_declined':
            await requests_page.edit(message=call.message, page_id=int(calling_data[1]), status='declined')
        case 'Request_info':
            await request_info.edit(message=call.message, request_id=calling_data[1])
        case 'Change_status':
            await change_status.edit(message=call.message, request_id=calling_data[1])
        case 'Changing_status':
            database_functions.update_request_status_by_id(request_id=int(calling_data[1]), status=calling_data[2])
            await requests_page.edit(message=call.message, page_id=0, status=calling_data[3])
        case _:
            await bot.send_message(chat_id=call.message.chat.id, text='Incorrect callback try /start')


asyncio.run(bot.polling(none_stop=True, timeout=0))
