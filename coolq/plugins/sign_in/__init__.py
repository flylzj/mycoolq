# coding: utf-8
from nonebot import on_command, require
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.log import logger
import json
from coolq.util.coolq import get_coolq_bot
from .resource import SignInResource

t00ls_add = on_command("t00ls_add", aliases={"土司账号添加"})


@t00ls_add.handle()
async def t00ls_add_command(bot: Bot, event: Event, state: T_State):
    # 消息至少需要传入三个参数 账号，密码md5，密保问题编号，（密保答案（问题编号为0则不需要答案））
    arg_text = event.get_plaintext()
    args = arg_text.split(" ")
    if len(args) < 3:
        await bot.send(event, "参数错误")
        return

    user_id = event.get_user_id()
    sign_resource = SignInResource(user_id)
    message = sign_resource.t00ls_account_add(args[0], args[1], args[2], args[3] if len(args) > 3 else "")
    if message:
        await bot.send(event, message)


t00ls_fetch = on_command("t00ls_fetch", aliases={"土司账号列表"})


@t00ls_fetch.handle()
async def t00ls_fetch_command(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    sign_resource = SignInResource(user_id)
    message = sign_resource.get_t00ls_account()
    if message:
        await bot.send(event, message)


t00ls_modify = on_command("t00ls_modify", aliases={"土司账号修改"})


@t00ls_modify.handle()
async def t00ls_modify_command(bot: Bot, event: Event, state: T_State):
    arg_text = event.get_plaintext()
    args = arg_text.split(" ")
    if len(args) < 4 or not args[0].isalpha():
        await bot.send(event, "参数错误")
        return
    user_id = event.get_user_id()
    sign_resource = SignInResource(user_id)
    message = sign_resource.t00ls_account_update(
        int(args[0]),
        username=args[1],
        password=args[2],
        questionid=args[3],
        answer=args[4] if len(args) > 4 else ""
    )
    if message:
        await bot.send(event, message)


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', second="0-59/10")
async def t00ls_sign_in():
    bot = get_coolq_bot()
    for r in SignInResource.get_all_t00ls_account():
        logger.debug(f"start sign in id {r.id} account {r.account_info}")
        account_info = json.loads(r.account_info)
        res = await SignInResource.t00ls_sign_in(account_info=account_info)
        if res:
            await bot.send_private_msg(user_id=r.user_id, message=f"{account_info.get('username')}签到成功")
        else:
            await bot.send_private_msg(user_id=r.user_id, message=f"{account_info.get('username')}签到失败")
