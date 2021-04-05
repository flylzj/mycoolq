# coding: utf-8
import nonebot


nonebot.init(apscheduler_autostart=True)
nonebot.load_plugins("coolq_nonebot2/plugins")

app = nonebot.get_asgi()

if __name__ == '__main__':
    nonebot.run()