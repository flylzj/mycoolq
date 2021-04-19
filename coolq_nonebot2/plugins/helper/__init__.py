# coding: utf-8
import nonebot
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


helper = nonebot.on_command('help', aliases={"帮助", })


@helper.handle()
async def handle_help(bot: Bot, event: Event, state: T_State):
    message = '''
    命令列表
    标准库---查看python标准库
    教程传送门---查看推荐教程
    语言参考--查看python语言参考文档
    试着发送"教程传送门"
    '''
    await bot.send(event, message)
