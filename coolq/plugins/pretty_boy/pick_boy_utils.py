import random

import nonebot
from nonebot.adapters.cqhttp import Bot
from coolq.plugins.pretty_boy.config import CustomConfig
from nonebot.adapters.cqhttp.message import Message
from coolq.plugins.pretty_boy.redis_utils import Redis
from nonebot.log import logger


async def base(group_id, bot_id):
    bot: Bot = nonebot.get_bots()[bot_id]
    sex, user_id = get_today_pretty_boy()
    logger.info(f"the boy {user_id}")
    message = f'今日{sex}诞生啦！{user_id}' + Message(f'[CQ:at,qq={user_id}]')
    return await bot.call_api('send_group_msg', **{
        'group_id': group_id,
        'message': message
    })


def check_boy(boys):
    man_list = list(filter(lambda x: x["sex"] != "unknown", boys))
    pretty_boy = random.choice(man_list)
    sex_code = pretty_boy["sex"]
    user_id = pretty_boy["user_id"]
    sex = "靓仔" if sex_code == "male" else "靓妞"
    return sex, user_id


def get_today_pretty_boy():
    """
    获取今天的pretty_boy
    :return:
    """
    key = CustomConfig.pretty_boy_key
    user_id = Redis.hget(key, "user_id")
    sex = Redis.hget(key, "sex")
    if user_id is not None and sex is not None:
        return sex, user_id
    bot: Bot = nonebot.get_bots()[CustomConfig.bot_id]
    boys = await bot.call_api('get_group_member_list', **{'group_id': CustomConfig.group_id})

    sex, user_id = check_boy(boys)
    Redis.hset(key, "user_id", user_id)
    Redis.hset(key, "sex", sex)
    return sex, user_id
