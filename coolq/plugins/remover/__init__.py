from nonebot import get_bot, on_notice, NoticeSession, on_command, CommandSession, on_request, RequestSession
import nonebot
import time
from config import MANAGING_GROUPS, QQ_GROUP_CAPTCHA_HINT_IMG
from coolq.db.model.new_member_captcha import gen_code, insert_new_captcha, verify, find_out_date


# remove a member every day
@nonebot.scheduler.scheduled_job('cron', day="1-31/1")
async def remove():
    bot = get_bot()
    for g in MANAGING_GROUPS:
        await _remove(bot, g)

async def _remove(bot: nonebot.NoneBot, group_id: str):
    members = await bot.get_group_member_list(group_id=group_id)
    long_time_no_speak_func = lambda item: time.time() - item.get('last_sent_time') > 2592000 and item.get('role') == 'member'
    long_time_no_speak_member = list(filter(long_time_no_speak_func, members))
    if long_time_no_speak_member:
        m = long_time_no_speak_member.pop()
        await bot.set_group_kick(group_id=group_id, user_id=m.get('user_id'), reject_add_request=False)
        message = "群友 {} 由于超过2592000秒未发言已被移出该群".format(m.get('nickname'))
        await bot.send_group_msg(group_id=group_id, message=message)


# ask some question to judge if he is a bot
@on_notice('group_increase')
async def new_member(session: NoticeSession):
    group_id = session.ctx['group_id']
    if session.ctx['group_id'] in MANAGING_GROUPS:
        user_id = session.ctx['user_id']
        code = gen_code()
        new = "[CQ:at,qq={}]".format(user_id)
        message = "{}欢迎入群！本群不留广告机器人，请在五分钟内复制“验证码 {}”并发送，否则将会被移出该群！。如有疑惑，可点击{}查看发送格式".format(new, code, QQ_GROUP_CAPTCHA_HINT_IMG)
        insert_new_captcha(
            group_id=group_id,
            user_id=user_id,
            verify_code=code,
            insert_time=int(time.time())
        )
        await session.send(message)


@on_command('captcha', aliases=('验证码', ), only_to_me=False)
async def verify_captcha(session: CommandSession):
    group_id = session.ctx['group_id']
    # not group message
    if session.ctx['message_type'] != 'group' or group_id not in MANAGING_GROUPS:
        return
    code = session.get('code', prompt='验证码错误')
    await session.send(verify(group_id, session.ctx['user_id'], code))


@verify_captcha.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['code'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请输入正确的验证码')
    session.state[session.current_key] = stripped_arg


# check if any captcha out of date
@nonebot.scheduler.scheduled_job('cron', minute="0-59/1")
async def check_out_date():
    session, members = find_out_date()
    if not members:
        return
    bot = get_bot()
    for member in members:
        # check is this member still in this group
        try:
            member_info = await bot.get_group_member_info(group_id=member.group_id, user_id=member.user_id)
        except Exception as e:
            member_info = {}
        if member_info.get('user_id'):
            message = "{}由于五分钟内没有发送验证码被移出该群".format(member.user_id)
            await bot.set_group_kick(group_id=member.group_id, user_id=member.user_id)
            await bot.send_group_msg(group_id=member.group_id, message=message)
        member.is_verify = 1
        session.commit()
    session.close()


@on_request('group')
async def apply(session: RequestSession):
    if session.ctx['group_id'] in MANAGING_GROUPS:
        await session.approve()






