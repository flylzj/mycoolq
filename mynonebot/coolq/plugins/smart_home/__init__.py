# coding: utf-8
from nonebot import logger, on_command, get_driver
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters import Bot, Event, Message
from nonebot.log import logger


from .config import Config
from .pc_switch import PcSwitch

global_config = get_driver().config
plugin_config = Config(**global_config.dict())


my_pc_command = on_command("mypc", aliases={"我的电脑"}, permission=SUPERUSER)


@my_pc_command.handle()
async def my_pc_command_handle(bot: Bot, event: Event, state: T_State):
    switch = PcSwitch(plugin_config.hass_host, plugin_config.hass_token)
    message = await switch.get_all_pc_states()
    await my_pc_command.finish(message)


turn_on_pc_command = on_command("turn_on_pc", aliases={"打开电脑"}, permission=SUPERUSER)


@turn_on_pc_command.handle()
async def turn_on_pc_handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if not args:
        await turn_on_pc_command.finish("未指明电脑")
    switch = PcSwitch(plugin_config.hass_host, plugin_config.hass_token)
    message = await switch.turn_on_off_pc(args, switch.TURN_ON)
    await turn_on_pc_command.finish(message)


turn_off_pc_command = on_command("turn_off_pc", aliases={"关闭电脑"}, permission=SUPERUSER)


@turn_off_pc_command.handle()
async def turn_off_pc__handle(bot: Bot, matcher: Matcher, args: Message = CommandArg()):
    pc_id = args.extract_plain_text()
    if not pc_id:
        await turn_off_pc_command.finish("未指明电脑")
    logger.info("turn_off_pc " + pc_id)
    switch = PcSwitch(plugin_config.hass_host, plugin_config.hass_token)
    message = await switch.turn_on_off_pc(pc_id, switch.TURN_OFF)
    await turn_off_pc_command.finish(message)

