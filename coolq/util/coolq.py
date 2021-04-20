# coding: utf-8
import nonebot
from nonebot.log import logger
from nonebot.adapters.cqhttp import Bot


def get_coolq_bot(bot_id="") -> Bot:
    try:
        if bot_id == "":
            bot: Bot = nonebot.get_bots().popitem()[1]
            # 暂时没有接多bot的想法，先写死bot
            return bot
        bot = nonebot.get_bots()[bot_id]
        return bot
    except Exception as e:
        logger.error("get_bot err {}".format(str(e)), exc_info=True)
        return None
