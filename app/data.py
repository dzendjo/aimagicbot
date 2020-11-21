from jinja2 import Environment
from j2tools import YamlLoader
from collections import OrderedDict
from contextvars import ContextVar
import pytz
import re
import os


jinja = Environment(loader=YamlLoader('templates.yml'))

process_images = ['🌇', '🌆', '🏙']

ai_api_key = '46d90da1-985c-44a9-9841-d7f45770df2f'

improve_url = 'https://api.deepai.org/api/torch-srgan'
colorize_url = 'https://api.deepai.org/api/colorizer'

# Database
DB_HOST = os.environ.get('DB_HOST', 'mongo')
DB_NAME = os.environ.get('DB_NAME', 'aimagicbot')
DB_PORT = int(os.environ.get('DB_PORT', 27017))

# Translation function
current_T = ContextVar('current_T')
get_t = None
# context2 = ContextVar('context2')

current_user = ContextVar('current_user')

default_lang = 'ru'

send_as_file_url = 'https://telegra.ph/file/de7645aa04ee086eae869.jpg'
