from data import jinja
from rocketgram import GetFile, context
from aiohttp import ClientSession, FormData
import requests
import datetime
import data
from models import User
import logging


logger = logging.getLogger('minibots.engine')


async def register_user(rg_user):
    now = datetime.datetime.now()

    user = User()
    user.id = rg_user.user_id
    user.created = now
    user.visited = now
    user.username = rg_user.username
    user.first_name = rg_user.first_name
    user.language_code = rg_user.language_code
    user.language = data.default_lang

    await user.commit()
    return user


async def upload_to_telegraph(file_id):
    response = await GetFile(file_id).send()
    API_FILE_URL = 'https://api.telegram.org/file/bot{}/'.format(context.bot.token)
    url = API_FILE_URL + response.result.file_path

    session: ClientSession = context.bot.connector._session

    response = await session.get(url)
    file_data = await response.read()

    form = FormData()
    form.add_field('file', file_data)

    async with session.post('https://telegra.ph/upload', data=form) as response:
        resp = await response.json()
        if 'error' in resp:
            logger.error(resp)
            return resp
        else:
            p = (await response.json())[0]['src']
            attach = f'https://telegra.ph{p}'
            return attach


async def improve_resolution(image_url):
    pass


async def image_colorize(image_url):
    pass
