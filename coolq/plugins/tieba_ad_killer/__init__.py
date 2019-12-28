# coding: utf-8
from nonebot import get_bot
from .tieba import get_tid
import re

bot = get_bot()

@bot.on_message()
async def _(ctx):
    '''

    :param ctx:
    :return:
    '''
    msg = ctx.get("message")[0]
    if msg.get('type') == 'rich':
        data = msg.get('data')
        try:
            u = re.search(r'jumpUrl":"(http[s]?://url.cn/.+?)"', data.get('content'))
            url = u.groups()[0]
            tid = await get_tid(url)
            await bot.send(ctx, "解析出tid为{},等待下次任务删除".format(tid))
        except Exception as e:
            print(e)