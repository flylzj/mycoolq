from nonebot.message import event_preprocessor
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
from nonebot.typing import T_State
from coolq.util.downloader import download_image


@event_preprocessor
async def voice2text(bot: Bot, event: Event, state: T_State):
    if not isinstance(event, MessageEvent) or event.message_type != 'private':
        return
    
    for m in event.get_message():
        if m.data.get("file") and "image" in m.data.get("file"):
            downloaded_file = await download_image(m.data.get("url"), m.data.get("file"))
            with open(downloaded_file, 'rb') as f:
                reply_message = Message(
                    MessageSegment.image(f.read())
                )
            await bot.send(event, message=reply_message)
            return