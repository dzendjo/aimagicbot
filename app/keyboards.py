from mybot import router
from rocketgram import MessageType, InlineKeyboard
from rocketgram import context, commonfilters, ChatType, SendMessage
import data



async def get_process_photo_ik(telegraph_id):
    T = data.current_T.get()
    kb = InlineKeyboard()

    text = T('process_kb/colorize')
    kb.callback(text, f'colorize {telegraph_id}').row()

    text = T('process_kb/improve')
    kb.callback(text, f'send_as_file {telegraph_id}').row()

    # text = T('process_kb/improve')
    # kb.callback(text, f'improve {telegraph_id}').row()

    return kb


async def get_process_document_ik(telegraph_id):
    T = data.current_T.get()
    kb = InlineKeyboard()

    text = T('process_kb/colorize')
    kb.callback(text, f'colorize {telegraph_id}').row()

    text = T('process_kb/improve')
    kb.callback(text, f'improve {telegraph_id}').row()

    return kb


async def get_send_as_file_ik(telegraph_id):
    T = data.current_T.get()
    kb = InlineKeyboard()

    kb.callback(T('send_as_file/use_this'), f'improve {telegraph_id}').row()
    kb.callback(T('send_as_file/use_file'), 'send_as_file_info').row()

    return kb

