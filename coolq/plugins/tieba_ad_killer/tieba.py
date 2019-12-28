# coding: utf-8
import aiohttp

async def get_tid(url):
    async with aiohttp.ClientSession() as http_session:
        async with http_session.get(url) as res:
            return res.url.path.split('/')[-1]

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    tasks = [get_tid("http://url.cn/5BUGoUZ")]
    loop.run_until_complete(asyncio.wait(tasks))