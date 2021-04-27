from nonebot import on_command
from nonebot.adapters.cqhttp import message
from nonebot.adapters.cqhttp.message import Message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp import GroupMessageEvent

from .crawler import get_setu
roll = on_command("setu", aliases={'涩图', '买家秀'}, priority=5)


@roll.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: T_State):
    setu = await get_setu()
    await roll.send(Message(f'[CQ:image,file={setu}]'))