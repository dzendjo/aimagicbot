from mybot import router
from rocketgram import InlineKeyboard
from rocketgram import SendMessage, AnswerCallbackQuery, SendPhoto, SendDocument
from rocketgram import commonfilters, ChatType, context2, EditMessageText
import aiohttp, asyncio
import data
from models import User
from data import jinja, process_images
from keyboards import get_send_as_file_ik
import logging


logger = logging.getLogger('minibots.engine')


async def send_process_message(chat_id):
    user = await User.find_one(chat_id)
    T = data.current_T.get()
    process_text = T('process')
    add_process_text = T('add_process')
    dots = 1
    img_index = 0
    mt = process_images[img_index] + ' ' + process_text + '.' * dots + add_process_text
    resp = await SendMessage(chat_id, mt).send2()
    while True:
        if user.process_flag:
            await asyncio.sleep(1)
            user = await User.find_one(chat_id)
            img_index = img_index + 1 if img_index < len(process_images) - 1 else 0
            dots = dots + 1 if dots < 3 else 1
            mt = process_images[img_index] + " " + process_text + '.' * dots + add_process_text
            await EditMessageText(mt, chat_id, resp.message_id).send2()
        else:
            await EditMessageText(T('task_complete'), chat_id, resp.message_id).send2()
            return resp.message_id


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.callback('colorize')
async def reaction_on_colorized():
    await AnswerCallbackQuery(context2.callback.query_id).send2()
    user = await User.find_one(context2.user.user_id)
    telegraph_id = context2.callback.data.split()[1]
    image_url = f'https://telegra.ph/file/{telegraph_id}.jpg'
    T = data.current_T.get()

    user.process_flag = True
    await user.commit()
    task = asyncio.create_task(send_process_message(context2.user.user_id))

    async with aiohttp.ClientSession() as session:
        headers = {'api-key': data.ai_api_key}
        async with session.post(data.colorize_url, data={'image': image_url}, headers=headers) as response:
            try:
                resp = await response.json()
                out_image_url = resp['output_url']
                await SendPhoto(context2.user.user_id, out_image_url).send2()
                await SendDocument(context2.user.user_id, out_image_url, caption=T('full_quality')).send2()
            except Exception as e:
                logger.error(resp)
                await SendMessage(context2.user.user_id, T('errors/process')).send2()

    user.process_flag = False
    await user.commit()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.callback('improve')
async def reaction_on_improve():
    await AnswerCallbackQuery(context2.callback.query_id).send2()
    user = await User.find_one(context2.user.user_id)
    telegraph_id = context2.callback.data.split()[1]
    image_url = f'https://telegra.ph/file/{telegraph_id}.jpg'
    T = data.current_T.get()

    user.process_flag = True
    await user.commit()
    task = asyncio.create_task(send_process_message(context2.user.user_id))

    async with aiohttp.ClientSession() as session:
        headers = {'api-key': data.ai_api_key}
        async with session.post(data.improve_url, data={'image': image_url}, headers=headers) as response:
            try:
                resp = await response.json()
                out_image_url = resp['output_url']
                await SendDocument(context2.user.user_id, out_image_url).send2()
                await SendMessage(context2.user.user_id, T('post_mt')).send2()
            except Exception as e:
                await SendMessage(context2.user.user_id, T('errors/process')).send2()

    user.process_flag = False
    await user.commit()




@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.callback('send_as_file')
async def reaction_on_suggest():
    await AnswerCallbackQuery(context2.callback.query_id).send2()
    telegraph_id = context2.callback.data.split()[1]
    T = data.current_T.get()
    kb = await get_send_as_file_ik(telegraph_id)
    await SendMessage(context2.user.user_id, T('send_as_file/mt'), reply_markup=kb.render()).send2()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.callback('send_as_file_info')
async def reaction_on_suggest():
    await AnswerCallbackQuery(context2.callback.query_id).send2()
    T = data.current_T.get()
    await SendMessage(context2.user.user_id, T('send_as_file/use_file_mt'), disable_web_page_preview=False).send2()


