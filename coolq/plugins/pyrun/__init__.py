# coding: utf-8
from nonebot.log import logger
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State


def custom_exec(code):
    try:
        return exec(code, {}, {})
    except Exception as e:
        logger.error(f"custom_exec err {str(e)}")
        return "执行失败"


pyrun = on_command("pyrun")


@pyrun.handle()
async def run_code(bot: Bot, event: Event, state: T_State):
    arg_text = event.get_message()
    await bot.send(event, custom_exec(arg_text))