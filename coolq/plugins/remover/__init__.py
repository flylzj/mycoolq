from nonebot import get_bot, on_notice, NoticeSession, on_command, CommandSession, on_request, RequestSession
import nonebot
import time
from config import MANAGING_GROUPS, QQ_GROUP_CAPTCHA_HINT_IMG
from coolq.util.coolq import at_someone


# remove a member every day
# @nonebot.scheduler.scheduled_job('cron', day="1-31/1")
# async def remove():
#     bot = get_bot()
#     for g in MANAGING_GROUPS:
#         await _remove(bot, g)
#
#
# async def _remove(bot: nonebot.NoneBot, group_id: str):
#     members = await bot.get_group_member_list(group_id=group_id)
#     long_time_no_speak_func = lambda item: time.time() - item.get('last_sent_time') > 2505600 and item.get('role') == 'member'
#     long_time_no_speak_member = list(filter(long_time_no_speak_func, members))
#     if long_time_no_speak_member:
#         m = long_time_no_speak_member.pop()
#         await bot.set_group_kick(group_id=group_id, user_id=m.get('user_id'), reject_add_request=False)
#         message = "群友 {} 由于超过2505600秒未发言已被移出该群".format(m.get('nickname'))
#         await bot.send_group_msg(group_id=group_id, message=message)


# ask some question to judge if he is a bot
@on_notice('group_increase')
async def new_member(session: NoticeSession):
    if session.ctx['group_id'] in MANAGING_GROUPS:
        # group_id = session.ctx['group_id']
        user_id = session.ctx['user_id']
        message = f"{at_someone(user_id)}欢迎入群, 配置环境、安装第三方库、IDLE / VSCode / Pycharm的使用、调试、运行代码等问题参考群文件“从零开始的Python环境配置.rar”。Python安装包、VSCode安装包、Pycharm安装包都可以在群文件找到，按需自取。试着对我说:help"
        # user_id = session.ctx['user_id']
        # code = gen_code()
        # new = "[CQ:at,qq={}]".format(user_id)
        # message = "{} 欢迎入群！\n请在五分钟内私聊我\n“验证码 {}”\n否则会被视为机器人并移出本群。".format(new, code)
        # insert_new_captcha(
        #     group_id=group_id,
        #     user_id=user_id,
        #     verify_code=code,
        #     insert_time=int(time.time())
        # )
        # await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=300)
        await session.send(message)


# @on_command('captcha', aliases=('验证码', ), only_to_me=False)
# async def verify_captcha(session: CommandSession):
#     # group_id = session.ctx['group_id']
#     # not group message
#     # if session.ctx['message_type'] != 'group' or group_id not in MANAGING_GROUPS:
#     #     return
#     code = session.get_optional('code')
#     user_id = session.ctx['user_id']
#     group_id = verify(user_id, code)
#     if group_id:
#         message = "验证成功, 环境问题参考群文件“从零开始的Python环境配置.rar”。Python安装包、VSCode安装包、Pycharm安装包都可以在群文件找到，按需自取。试着对我说:help"
#         await session.bot.set_group_ban(group_id=group_id, user_id=user_id, duration=0)
#     else:
#         message = "验证码错误或者不存在"
#     await session.send(message)


# @verify_captcha.args_parser
# async def _(session: CommandSession):
#     stripped_arg = session.current_arg_text.strip()
#
#     if session.is_first_run:
#         if stripped_arg:
#             session.state['code'] = stripped_arg
#         return
#
#     if not stripped_arg:
#         session.pause('请输入正确的验证码')
#     session.state[session.current_key] = stripped_arg


# check if any captcha out of date
# @nonebot.scheduler.scheduled_job('cron', minute="0-59/1")
# async def check_out_date():
#     session, members = find_out_date()
#     if not members:
#         return
#     bot = get_bot()
#     for member in members:
#         # check is this member still in this group
#         try:
#             member_info = await bot.get_group_member_info(group_id=member.group_id, user_id=member.user_id)
#         except Exception as e:
#             member_info = {}
#         if member_info.get('user_id'):
#             message = "{}由于五分钟内没有发送验证码被移出该群".format(member.user_id)
#             await bot.set_group_kick(group_id=member.group_id, user_id=member.user_id)
#             await bot.send_group_msg(group_id=member.group_id, message=message)
#         member.is_verify = 1
#         session.commit()
#     session.close()


# @on_request('group')
# async def apply(session: RequestSession):
#     if session.ctx['group_id'] in MANAGING_GROUPS:
#         await session.approve()






