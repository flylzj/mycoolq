# coding: utf-8
import nonebot
from nonebot.typing import Context_T
from coolq.db.model.new_member_captcha import is_verifying
from config import QQ_GROUP_CAPTCHA_HINT_IMG

bot = nonebot.get_bot()

@bot.on_message('group')
async def handle_group_message(ctx: Context_T):
    group_id = ctx.get('group_id')
    user_id = ctx.get('user_id')
    if is_verifying(group_id, user_id):
        try:
            from_message: str = str(ctx.get('message'))
            if not from_message.startswith('验证码') or not from_message.strip('验证码 ').isdigit():
                new = "[CQ:at,qq={}]".format(user_id)
                message = "{}请输入正确的验证格式为：验证码 123456(注意中间的空格)\n可以点击链接查看格式{}".format(new, QQ_GROUP_CAPTCHA_HINT_IMG)
                await bot.send(ctx, message)
        except Exception as e:
            bot.logger.info(e)
            pass