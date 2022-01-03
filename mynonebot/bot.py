# coding: utf-8
from os import path

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_builtin_plugins()

if __name__ == "__main__":
    nonebot.load_plugins(
        path.join(path.dirname(__file__), "coolq", "plugins")
    )
    nonebot.run(host="0.0.0.0", port=8080)