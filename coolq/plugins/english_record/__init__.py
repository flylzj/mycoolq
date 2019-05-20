# coding: utf-8
from config import SESSION
from nonebot import get_bot
from coolq.db.model.english_record import EnglishRecord, EnglishUser, search_history, count_recorded, get_statistics_data, search_user
from coolq.plugins.english_record.record_charts import render_english_record_data
import aiohttp
from bs4 import BeautifulSoup
import time
import re

bot = get_bot()


async def get_english_record(url, share=True):
    async with aiohttp.ClientSession() as http_session:
        async with http_session.get(url) as res:
            soup = BeautifulSoup(await res.text(), 'html.parser')
            nums = soup.find('p', attrs={'id': 'today', 'class': 'num-roll'})['data-num']
            days = soup.find('p', attrs={'id': 'days', 'class': 'num-roll'})['data-num']
            if share:
                return nums, days
            else:
                # 返回重定向之后的url
                return nums, days, res.url.human_repr()


@bot.on_message()
async def _(ctx):
    '''
    :param ctx: {"user_id": "", "sender": {"nickname": ""}}:
    :return:
    '''
    msg = ctx.get("message")[0]
    user_id = ctx.get('user_id')
    nickname = ctx.get('sender').get('nickname')
    is_record = False
    if msg.get("type") == 'share':
        data = msg.get('data')
        if 'http://learn.baicizhan.com/daka_page/qzone' in data.get('url'):
            is_record = True
            url = data.get('url')
            nums, days = await get_english_record(url)
        else:
            return
    elif msg.get('type') == 'rich':
        data = msg.get('data')
        if "百词斩" in data.get('title'):
            is_record = True
            url = re.search(r'"jumpUrl":"(url.cn/.*?)"', data.get('content'))
            if not url:
                return
            url = url.groups()[0]
            url = "https://" + url
            nums, days, url = await get_english_record(url, share=False)
        else:
            return
    else:
        return

    if is_record:
        user = search_user(str(user_id))
        try:
            session = SESSION()
            if not user:
                u = EnglishUser(
                    user_id=user_id,
                    nickname=nickname
                )
                session.add(u)
            else:
                user.nickname = nickname
            session.commit()
            session.close()
        except Exception as e:
            bot.logger.error(e)
            await bot.send(ctx, message="发生错误{}".format(e))
        res = search_history(url)
        if res:
            await bot.send(ctx, message="哼！还想拿以前的打卡来糊弄人~")
            return
        try:
            record = EnglishRecord(
                user_id=str(user_id),
                word_count=int(nums),
                days=int(days),
                url=url,
                record_datetime=int(time.time())
            )
            session = SESSION()
            session.add(record)
            session.commit()
        except Exception as e:
            bot.logger.error(e)
        word_count, days_this_month, days_total = count_recorded(str(user_id))
        msg = "打卡统计：\n本月单词数量: {}\n本月打卡数量: {}\n总打卡数量: {}\n统计图: {}\n".format(
            word_count, days_this_month, days_total, "http://120.24.66.220:8081/render.html") \
              + "[CQ:at,qq={}]".format(user_id)
        render_english_record_data(get_statistics_data())
        await bot.send(ctx, message=msg)


