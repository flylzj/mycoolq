# coding: utf-8
import nonebot

bot = nonebot.get_bot()

# @bot.on_message('private')
# async def handle_captcha_message(ctx: Context_T):
#     user_id = ctx.get('user_id')
#     nmc = is_verifying(user_id)
#     if nmc:
#         try:
#             from_message: str = str(ctx.get('message'))
#             if not from_message.startswith('验证码 ') or not from_message.strip('验证码 ').isdigit():
#                 code = nmc.verify_code
#                 message = "请输入正确的验证格式为：验证码 {}(注意中间的空格)\n可以点击链接查看格式{}".format(code, QQ_GROUP_CAPTCHA_HINT_IMG)
#                 await bot.send(ctx, message)
#         except Exception as e:
#             bot.logger.info(e)
#             await bot.send(ctx, str(e))