# coding: utf-8
from nonebot import on_command, CommandSession
import nonebot


@on_command('help', aliases=("帮助"), only_to_me=False)
def helper(session: CommandSession):
    pass


