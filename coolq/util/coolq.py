# coding: utf-8
import nonebot
from nonebot.log import logger
from nonebot.adapters.cqhttp.exception import ActionFailed, NetworkError


class CoolqBot(object):
    group_api = "send_group_msg"
    private_api = "send_private_msg"

    def __init__(self, bot_id="", bot=None):
        if bot:
            self.bot = bot
        else:
            self.bot = self.get_bot(bot_id)

    @staticmethod
    def get_bot(bot_id=""):
        try:
            if bot_id == "":
                bots = list(nonebot.get_bots().items())
                if len(bots) == 0:
                    return None
                # 暂时没有接多bot的想法，先写死bot
                bot = bots[0][1]
                return bot
            bot = nonebot.get_bots()[bot_id]
            return bot
        except Exception as e:
            logger.error("get_bot err {}".format(str(e)), exc_info=True)
            return None

    async def get_group_user_nickname(self, group_id, user_id):
        logger.debug("get_group_user_nickname group_id {} user_id {}".format(group_id, user_id))
        try:
            res = await self.bot.call_api(
                "get_group_member_info",
                **{
                    "group_id": group_id,
                    "user_id": user_id
                }
            )
            return res
        except Exception as e:
            logger.error("get_group_user_nickname err {}".format(str(e)))
            return ""

    async def send_private_message(self, message, user_id):
        try:
            await self.bot.call_api(self.private_api, **{
                "message": message,
                "user_id": user_id
            })
        except ActionFailed as e:
            logger.error("send_private_message action err {}".format(str(e)))
        except NetworkError as e:
            logger.error("send_private_message network err {}".format(str(e)))

    async def send_group_message(self, message, group_id):
        try:
            await self.bot.call_api(self.group_api, **{
                "message": message,
                "group_id": group_id
            })
        except ActionFailed as e:
            logger.error("send_group_message action err {}".format(str(e)))
        except NetworkError as e:
            logger.error("send_group_message network err {}".format(str(e)))
