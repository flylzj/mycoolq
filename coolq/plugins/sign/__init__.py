# coding: utf-8
from nonebot import get_bot
from .sentence import get_sentence


bot = get_bot()


@bot.on_message()
async def _(ctx):
    msg = ctx.get("message")[0]
    if msg.get("type") == 'sign':
        print(dict(msg))
        data = msg.get("data").get("title")
        if "宜" in data:
            data = data.strip("宜 ")
            s = await get_sentence(data)
            if s:
                await bot.send(ctx, message=s)