from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from .crawler import get_chp


MAX_COUNT = 10
MIN_COUNT = 1

chp = on_command("彩虹屁", aliases={'chp', 'p', '放屁', '屁'}, rule=to_me())


@chp.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await bot.send(event, "1")
    print("111")
    count = str(event.get_message()).strip()
    if not count.isdigit() and count not in range(MIN_COUNT, MAX_COUNT):
        count = MIN_COUNT
    count = int(count)

    for _ in range(count):
        await chp.finish(await get_chp())