import aiohttp
import json
from nonebot.log import logger


async def get_chp():
    chp_url = 'https://api.muxiaoguo.cn/api/caihongpi'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=chp_url) as r:
                data = await r.text()
                logger.info("chp text" + data)
                data = json.loads(data)
                content = data['data']['comment']
                if content:
                    return content
                return "彩虹屁出问题了"
        except Exception as e:
            logger.error("get_chp err" + str(e), exc_info=True)
            return "无屁可放"


if __name__ == '__main__':
    import asyncio
    print(asyncio.run(get_chp()))