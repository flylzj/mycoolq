# coding: utf-8
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from create_db import init_db

init_db()
nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_plugins("coolq/plugins")


if __name__ == '__main__':
    nonebot.run(host="0.0.0.0")