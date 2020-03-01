# coding: utf-8
import nonebot
from nonebot.typing import Context_T
from config import MANAGING_GROUPS
from coolq.db.model.new_member_captcha import is_verifying

bot = nonebot.get_bot()

@bot.on_message('group')
async def handle_group_message(ctx: Context_T):
    group_id = ctx.get('group_id')
    user_id = ctx.get('user_id')
    if is_verifying(group_id, user_id):
        message = "请输入正确的验证格式为：验证码 123456"
        await bot.send(ctx, message)