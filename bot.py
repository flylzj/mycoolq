# coding: utf-8
import nonebot
import os
import config
from create_db import init_db


if __name__ == '__main__':
    nonebot.init(config)
    init_db()
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'coolq', 'plugins'),
        'coolq.plugins'
    )
    nonebot.run(host='0.0.0.0', port=8080)