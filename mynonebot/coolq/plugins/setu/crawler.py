import aiohttp
from nonebot.log import logger
import json



async def get_setu(token):
    # 淘宝买家秀图片
    setu_url = 'https://api.sumt.cn/api/rand.tbimg.php?format=json&token={}'.format(token)
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
                return 'https://gw1.alicdn.com//tfscom//tuitui//O1CN01icPlfu1FLIcwYf4r9_!!0-rate.jpg'
        except Exception as e:
            logger.error("get_setu err" + str(e), exc_info=True)
            return 'https://gw1.alicdn.com//tfscom//tuitui//O1CN01icPlfu1FLIcwYf4r9_!!0-rate.jpg'
