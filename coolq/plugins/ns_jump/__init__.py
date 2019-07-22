# coding: utf-8
from nonebot import on_command, CommandSession
from .jump import search_game, get_game_detail


@on_command('ns_jump', aliases=('ns', ), only_to_me=False)
async def ns_jump_command(session: CommandSession):
    title = session.get('title', prompt="请输入要查询的游戏作为参数")

    try:
        res = await search_game(title)
    except Exception as e:
        res = str(e)
    await session.send(res)


@ns_jump_command.args_parser
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()

    if session.is_first_run:
        if arg:
            session.state['title'] = arg
        return

    if not arg:
        session.pause('要查询的游戏名称不能为空呢，请重新输入')

    session.state[session.current_key] = arg


@on_command('ns_jump_game', aliases=('nsgame', ), only_to_me=False)
async def ns_jump_game_command(session: CommandSession):
    appid = session.get('appid', prompt="请输入要查询的游戏作为参数")

    try:
        res = await get_game_detail(appid)
    except Exception as e:
        res = str(e)
    await session.send(res)


@ns_jump_game_command.args_parser
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()

    if session.is_first_run:
        if arg:
            session.state['appid'] = arg
        return

    if not arg:
        session.pause('要查询的appid名称不能为空呢，请重新输入')

    session.state[session.current_key] = arg
