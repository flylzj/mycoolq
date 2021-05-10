from nonebot import on_command
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from .crawler import get_setu
from coolq.db.models import SetuHistory
import time

setu = on_command("setu", aliases={'涩图', '买家秀'}, priority=5)


@setu.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    setu_url = await get_setu()
    user_id = event.get_user_id()
    if SetuHistory.count_toady_setu(user_id=user_id) < 1:
        await bot.send(event, Message(f'[CQ:image,file={setu_url}]'))
        SetuHistory.insert_setu(user_id=user_id, setu_url=setu_url, create_time=int(time.time()))
    else:
        await bot.send(event, message="涩图伤身，一次只能一次哦")