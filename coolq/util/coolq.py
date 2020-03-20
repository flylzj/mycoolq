# coding: utf-8
from nonebot import get_bot

def at_someone(user_id):
    return f"[CQ:at,qq={user_id}]"


async def get_group_user_name(group_id, user_id):
    bot = get_bot()
    info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    if info.get('card'):
        return info.get('card')

    if info.get('nickname'):
        return info.get('card')

    return user_id