from mybot import router
from rocketgram import commonfilters, ChatType, SendMessage, EditMessageText
from rocketgram import context, MessageType
from data import jinja, process_images
import data
import tools
from models import User


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.command('/base')
async def start_command():
    T = data.current_T.get()
    count = await User.count_documents()
    await SendMessage(context.user.user_id, count).send()
