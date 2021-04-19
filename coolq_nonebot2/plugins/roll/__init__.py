# coding: utf-8
import time
import nonebot
from nonebot import on_command
from nonebot import require
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .config import Config
from .resource import RollResource
from coolq_nonebot2.util.coolq import CoolqBot


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

'''
2021.4.9
增加新功能
1.天选之人
每天只有一个人会触发天选之人事件，其得到的点数将为*正*且是点数的*三倍*

2.双倍时刻
每天固定/随机一个时间段，得到的点数为双倍（负数也会双倍）

3.勤劳之人
每天第一个肉必定为正且倍数双倍

4.管理buff
管理员生成的点数+6/-6(各占50%)

'''


roll = on_command("roll", aliases={"肉", })


@roll.handle()
async def handel_roll(bot: Bot, event: Event, state: T_State):
    '''
    :param bot: adapters.cqhttp.bot.Bot
    :param event: message.private.friend
    肉123
    event.get_type(): message
    event.get_user_id(): 732599980
    event.get_message() 123
    get_plaintext() 123
    get_event_description() Message -1014934360 from 732599980 "123"
    get_event_name() message.private.friend
    get_log_string() [message.private.friend]: Message -1014934360 from 732599980 "123"
    state.items() dict_items([('_prefix', {'raw_command': '肉', 'command': ('肉',)}), ('_suffix', {'raw_command': None, 'command': None})])
    event.dict()
    {
        'time': 1618627734,
        'self_id': 1449902124,
        'post_type': 'message',
        'sub_type': 'normal',
        'user_id': 732599980,
        'message_type': 'group',
        'message_id': 2096235876,
        'message': [MessageSegment(type='text', data={'text': '123'})],
        'raw_message': '肉123',
        'font': 0,
        'sender':
            {
                'user_id': 732599980,
                'nickname': 'Boom3',
                'sex': 'unknown',
                'age': 0,
                'card': '',
                'area': '',
                'level': '',
                'role': 'member',
                'title': ''
            },
        'to_me': False,
        'reply': None,
        'group_id': 1076038734,
        'anonymous': None,
        'message_seq': 1506
    }
    :param state:
    :return:
    '''
    roll_resource = RollResource(bot=bot, event=event)
    if roll_resource.can_roll_today():
        _, message = roll_resource.roll_with_event()
        if message:
            await bot.send(event, message)


roll_count = on_command("roll_count", aliases={"肉统计"})


@roll_count.handle()
async def roll_count_command(bot: Bot, event: Event, state: T_State):
    roll_resource = RollResource(bot=bot, event=event)
    message = await roll_resource.roll_count()
    if message:
        await bot.send(event, message)


my_roll = on_command("myroll", aliases={"我的肉"})


@my_roll.handle()
async def my_roll(bot: Bot, event: Event, state: T_State):
    roll_resource = RollResource(bot=bot, event=event)
    message = roll_resource.my_roll()
    if message:
        await bot.send(event, message)


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', **plugin_config.DOUBLE_ROLL_TIME_CRON)
async def increase_day():
    bot = CoolqBot()
    if bot.bot:
        for group_id in plugin_config.MANAGING_GROUPS:
            message = "双倍肉时刻开启，此时肉出的点数将翻倍"
            await bot.send_group_message(message, group_id)