# coding: utf-8
import nonebot
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .resource import get_chp


chp = nonebot.on_command('chp', aliases={"彩虹屁", })

MAX_COUNT = 5
MIN_COUNT = 1


@chp.handle()
async def handel_chp(bot: Bot, event: Event, state: T_State):
    count = str(event.get_message()).strip()
    if not count.isdigit() or int(count) not in range(MIN_COUNT, MAX_COUNT):
        count = MIN_COUNT
    count = int(count)
    for _ in range(count):
        await bot.send(event, await get_chp())


