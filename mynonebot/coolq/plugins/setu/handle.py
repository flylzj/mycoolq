from nonebot import on_command, get_driver
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters import Bot, Event
from .crawler import get_setu
from .config import Config

global_config = get_driver().config

plugin_config = Config(**global_config.dict())

setu = on_command("setu", aliases={'涩图', '买家秀'})


@setu.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    setu_url = await get_setu(plugin_config.setu_token)
    # user_id = event.get_user_id()
    await bot.send(event, Message(f'[CQ:image,file={setu_url}]'))
    # if SetuHistory.count_toady_setu(user_id=user_id) < 1:
        
    #     # SetuHistory.insert_setu(user_id=user_id, setu_url=setu_url, create_time=int(time.time()))
    # else:
    #     await bot.send(event, message="涩图伤身，一次只能一次哦")