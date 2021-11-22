from mybot import router
from rocketgram import commonfilters, ChatType, SendMessage, priority, SendSticker
from rocketgram import context
import data


@router.handler
@commonfilters.chat_type(ChatType.private)
@priority(2048)
def unknown():
    T = data.current_T.get()
    SendMessage(context.user.user_id, T('unknown')).webhook()
