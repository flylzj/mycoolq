# coding: utf-8
from nonebot import on_command, CommandSession


@on_command('help', aliases=("帮助"), only_to_me=False)
async def helper(session: CommandSession):
    message = '''
    命令列表
    标准库---查看python标准库
    肉---随机骰子点数
    教程传送门---查看推荐教程
    试着发送"教程传送门"
    '''
    await session.send(message)


