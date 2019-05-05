# coding: utf-8
from config import SESSION
from coolq.db.model.english_record import EnglishRecord
from nonebot import get_bot
import aiohttp
from bs4 import BeautifulSoup
import time

bot = get_bot()

async def get_english_record(url):
    async with aiohttp.ClientSession() as http_session:
        async with http_session.get(url) as res:
            soup = BeautifulSoup(await res.text(), 'html.parser')
            nums = soup.find('p', attrs={'id': 'today', 'class': 'num-roll'})['data-num']
            days = soup.find('p', attrs={'id': 'days', 'class': 'num-roll'})['data-num']
            return nums, days

def search_history(url):
    try:
        session = SESSION()
        res = session.query(EnglishRecord).filter_by(url=url).first()
        return res
    except Exception as e:
        bot.logger.error(e)

@bot.on_message()
async def _(ctx):
    msg = ctx.get("message")[0]
    if msg.get("type") == 'share':
        data = msg.get('data')
        if 'http://learn.baicizhan.com/daka_page/qzone' in data.get('url'):
            user_id = ctx.get('user_id')
            url = data.get('url')
            res = search_history(url)
            if res:
                await bot.send(ctx, message="哼！还想拿以前的打卡来糊弄人~")
                return
            nums, days = await get_english_record(url)
            record = EnglishRecord(
                user_id=user_id,
                word_count=nums,
                days=days,
                url=url,
                record_datetime=int(time.time())
            )
            try:
                session = SESSION()
                session.add(record)
                session.commit()
            except Exception as e:
                bot.logger.error(e)
            await bot.send(ctx, message="今日打卡完成")