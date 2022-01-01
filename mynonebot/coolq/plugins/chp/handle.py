from nonebot import on_command, CommandSession
from .crawler import get_chp


MAX_COUNT = 10
MIN_COUNT = 1


@on_command("彩虹屁", aliases={'chp', 'p', '放屁', '屁'})
async def handle_first_receive(session: CommandSession):
    count = session.current_arg_text.strip()
    if not count.isdigit() and count not in range(MIN_COUNT, MAX_COUNT):
        count = MIN_COUNT
    count = int(count)

    for _ in range(count):
        await session.send(await get_chp())


