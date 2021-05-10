# coding: utf-8
from nonebot.log import logger
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
import os
from threading import Thread
import random


def custom_exec(code):
    logger.debug(f"custom_exec cmd {code}")
    rand_filename = str(random.random()).split(".")[-1] + ".py"
    tmp_file = os.path.join("/tmp", rand_filename)

    def run_shell(cmd):
        res = os.popen(cmd).read()
        if not res:
            return "结果为空"
        return res
    try:
        with open(tmp_file, "w") as f:
            f.write(code)
        t = Thread(target=run_shell, args=(f"python {tmp_file}", ))
        t.start()

    except Exception as e:
        logger.error(f"custom_exec err {str(e)}")
        return "执行失败"
    finally:
        os.remove(tmp_file)


pyrun = on_command("pyrun")


@pyrun.handle()
async def run_code(bot: Bot, event: Event, state: T_State):
    arg_text = event.get_plaintext()
    logger.debug(f"arg text {arg_text}")
    await bot.send(event, custom_exec(arg_text))