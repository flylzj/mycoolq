from nonebot import get_bot
from config import REMOVER_GROUPS
import nonebot
import time


# remove a member every day
@nonebot.scheduler.scheduled_job('cron', day="1-31/1")
async def _():
    bot = get_bot()
    for g in REMOVER_GROUPS:
        await _remove(bot, g)

async def _remove(bot: nonebot.NoneBot, group_id: str):
    members = await bot.get_group_member_list(group_id=group_id)
    long_time_no_speak_func = lambda item: time.time() - item.get('last_sent_time') > 2592000 and item.get('role') == 'member'
    long_time_no_speak_member = list(filter(long_time_no_speak_func, members))
    if long_time_no_speak_member:
        m = long_time_no_speak_member.pop()
        # await bot.set_group_kick(group_id=group_id, user_id=m.get('user_id'), reject_add_request=False)
        message = "群友 {} 由于一个月未发言已被移出该群".format(m.get('nickname'))
        # await bot.send_group_msg(group_id=group_id, message=message)


