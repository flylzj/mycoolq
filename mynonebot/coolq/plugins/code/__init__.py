# coding: utf-8
from nonebot import on_command, CommandSession


@on_command("pyrun")
async def pyrun(session: CommandSession):
    arg_text = session.current_arg_text
    pass


def run_code(code):
    try:
        eval(code)
    except Exception as e:
        pass