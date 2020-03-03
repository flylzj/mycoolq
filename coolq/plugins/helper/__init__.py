# coding: utf-8
from nonebot import on_command, CommandSession


@on_command('help', aliases=("帮助"), only_to_me=False)
def helper(session: CommandSession):
    message = '''
    功能列表
    lib---查看python标准库
    roll---随机骰子点数
    '''
    session.send(message)


