# coding: utf-8
from nonebot import get_bot
import re


def get_user_id_group_id(session_id: str):
    if session_id.startswith("group"):
        ids = session_id.strip("_")
        return ids[1], ids[2]
    else:
        return 0, session_id


def at_someone(user_id):
    return f"[CQ:at,qq={user_id}]"


def parse_at_someone(text):
    user_ids_pattern = r"[CQ:at,qq=(\d{6,10})]"
    res = re.findall(user_ids_pattern, text)
    return res


async def get_group_user_name(group_id, user_id):
    bot = get_bot()
    info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    if info.get('card'):
        return info.get('card')

    if info.get('nickname'):
        return info.get('nickname')

    return user_id
