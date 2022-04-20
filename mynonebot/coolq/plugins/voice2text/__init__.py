from nonebot.message import event_preprocessor
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.typing import T_State


@event_preprocessor
async def voice2text(bot: Bot, event: Event, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    # for segment in event.message:
    #     print(segment)