# coding: utf-8
from nonebot import on_command, CommandSession
from .jump import search_game


@on_command('ns_jump', aliases=('ns', ), only_to_me=False)
async def ns_jump_command(session: CommandSession):
    title = session.get('title', prompt="请输入要查询的游戏作为参数")

    try:
        res = await search_game(title)
    except Exception as e:
        res = str(e)
    await session.send(res)


@ns_jump_command.args_parse
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()

    if session.is_first_run:
        if arg:
            session.state['title'] = arg
        return
