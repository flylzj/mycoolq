import aiohttp


async def get_chp():
    chp_url = 'https://api.muxiaoguo.cn/api/caihongpi'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=chp_url) as r:
            data = await r.json()
            content = data['data']['comment']
            if content:
                return content
            return "彩虹屁出问题了"