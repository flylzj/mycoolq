from nonebot import on_command
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from .crawler import get_setu

setu = on_command("setu", aliases={'涩图', '买家秀'}, priority=5)


@setu.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    setu_url = await get_setu()
    await bot.send(event, Message(f'[CQ:image,file={setu_url}]'))