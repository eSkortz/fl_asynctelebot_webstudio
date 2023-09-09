from telebot.async_telebot import AsyncTeleBot
import config


bot = AsyncTeleBot(f'{config.token}')


def get_text_from_status(status):
    match status:
        case 'new':
            return '🔔 Новая'
        case 'in_processing':
            return '📝 В обработке'
        case 'accepted':
            return '👨‍💻 Принята в работу'
        case 'declined':
            return '🗑 Отклонена'
        

def get_emoji_from_status(status):
    match status:
        case 'new':
            return '🔔'
        case 'in_processing':
            return '📝'
        case 'accepted':
            return '👨‍💻'
        case 'declined':
            return '🗑'
        

def get_caption_from_status(status):
    match status:
        case 'new':
            return '🔔  Список новых заявок 🔔'
        case 'in_processing':
            return '📝 Список заявок в обработке 📝'
        case 'accepted':
            return '👨‍💻 Список принятых заявок 👨‍💻'
        case 'declined':
            return '🗑 Список отколоненных заявок 🗑'

def get_call_keyword_from_status(status):
    match status:
        case 'new':
            return 'Requests_new'
        case 'in_processing':
            return 'Requests_in_processing'
        case 'accepted':
            return 'Requests_accepted'
        case 'declined':
            return 'Requests_declined'
        

async def delete_message(message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)