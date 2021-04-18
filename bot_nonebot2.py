# coding: utf-8
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
import coolq_nonebot2.db


nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_plugins("coolq_nonebot2/plugins")


if __name__ == '__main__':
    nonebot.run()