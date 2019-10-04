# coding: utf-8
from nonebot import on_command, CommandSession
from random import randint


@on_command('roll', aliases=('肉', ), only_to_me=False)
async def roll_command(session: CommandSession):
    message = "你肉到了{}点"
    roll = randint(1, 6)
    await session.send(message=message.format(roll))