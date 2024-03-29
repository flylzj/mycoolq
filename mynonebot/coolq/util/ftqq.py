# coding: utf-8
import aiohttp


async def send_msg_by_ftqq(key, title, desp):
    push_url = f"https://sctapi.ftqq.com/{key}.send"
    data = {
        "title": title,
        "desp": desp
    }
    async with aiohttp.ClientSession() as session:
        await session.post(push_url, data=data)


async def send_msg_by_wecomchan(push_url, key, msg):
    data = {
        "sendkey": key,
        "msg": msg,
        "msg_type": "text"
    }
    async with aiohttp.ClientSession() as session:
        await session.post(push_url, data=data)

