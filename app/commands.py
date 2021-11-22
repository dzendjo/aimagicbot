from mybot import router
from rocketgram import commonfilters, ChatType, SendMessage, EditMessageText
from rocketgram import context, MessageType
from data import jinja, process_images
import data
import tools
from keyboards import get_process_photo_ik, get_process_document_ik
from models import User


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.command('/start')
async def start_command():
    T = data.current_T.get()
    await SendMessage(context.user.user_id, T('start')).send2()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.message_type(MessageType.photo)
async def upload_photo():
    # Send upload message:
    T = data.current_T.get()
    mt = T('upload_image/uploading')
    resp = await SendMessage(context.user.user_id, mt).send2()

    link = await tools.upload_to_telegraph(context.message.photo[-1].file_id)
    print(link)
    telegraph_id = link.split('/')[-1].split('.')[0]

    # Edit message and choosing what to do
    mt = T('upload_image/done')
    kb = await get_process_photo_ik(telegraph_id)
    await EditMessageText(mt, context.user.user_id, resp.message_id, reply_markup=kb.render()).send2()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.message_type(MessageType.document)
async def upload_photo():
    # Send upload message:
    T = data.current_T.get()
    mt = T('upload_image/uploading')
    resp = await SendMessage(context.user.user_id, mt).send2()

    # Upload image to telegraph
    link = await tools.upload_to_telegraph(context.message.document.file_id)
    print(link)

    # Check errors
    if isinstance(link, dict):
        await SendMessage(context.user.user_id, T('errors/upload')).send2()
        return

    telegraph_id = link.split('/')[-1].split('.')[0]

    # Edit message and choosing what to do
    mt = T('upload_image/done')
    kb = await get_process_document_ik(telegraph_id)
    await EditMessageText(mt, context.user.user_id, resp.message_id, reply_markup=kb.render()).send2()
