import aiohttp
from nonebot.log import logger
import json


async def get_setu():
    # 淘宝买家秀图片
    setu_url = 'https://api.sumt.cn/api/rand.tbimg.php?format=json'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=setu_url) as r:
                data = await r.text()
                data = json.loads(data)
                logger.info("setu text" + str(data))
                if data['msg'] == 'success':
                    pic_url = data['pic_url']
                    return pic_url
                # 错误图片
                return 'http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg'
        except Exception as e:
            logger.error("get_setu err" + str(e), exc_info=True)
            return 'http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg'
