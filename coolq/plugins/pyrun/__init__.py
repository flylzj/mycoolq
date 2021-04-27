# coding: utf-8
from nonebot.log import logger
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State


def custom_exec(code):
    try:
        res = exec(code, {}, {})
        if not res:
            return "结果为空"
        return res
    except Exception as e:
        logger.error(f"custom_exec err {str(e)}")
        return "执行失败"


pyrun = on_command("pyrun")


@pyrun.handle()
async def run_code(bot: Bot, event: Event, state: T_State):
    arg_text = event.get_plaintext()
    logger.error(f"arg text {arg_text}")
    await bot.send(event, custom_exec(arg_text))