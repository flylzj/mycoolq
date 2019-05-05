# coding: utf-8
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
import aiohttp
from config import HWEATHER_KEY, WEATHER_CONFIG, WEATHER_TYPE, HWEATHER_API, BIG_FINGER_GROUP_ID


@nonebot.scheduler.scheduled_job('cron', hour="7", minute='30')
async def _():
    bot = nonebot.get_bot()
    for qq, loc in WEATHER_CONFIG.items():
        try:
            now_weather = await get_weather(WEATHER_TYPE.get('实况天气'), loc)
            forecast = await get_weather(WEATHER_TYPE.get('3-10天预报'), loc)
            lifestyle = await get_weather(WEATHER_TYPE.get('生活指数'), loc)
            msg = "天气：{}\n{}\n{}".format(now_weather, forecast, lifestyle) + "[CQ:at,qq={}]".format(qq)
            await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message=msg, auto_escape=False)
            # await bot.send_group_msg(group_id=, message="为了大拇指，记得去ta点赞")
        except CQHttpError as e:
            nonebot.logger.error(e, exc_info=True)


async def get_weather(weather_type, loc):
    async with aiohttp.ClientSession() as session:
        params = {
            "location": loc,
            "key": HWEATHER_KEY
        }
        async with session.get(HWEATHER_API.format(weather_type), params=params) as res:
            data = await res.json()
            data = data.get('HeWeather6')[0]
            if weather_type == 'now':
                return "实况天气：{}，{}，{}℃，{}{}级".format(
                    data.get('basic').get('location'),
                    data.get('now').get('cond_txt'),
                    data.get('now').get('fl'),
                    data.get('now').get('wind_dir'),
                    data.get('now').get('wind_sc')
                )
            elif weather_type == 'forecast':
                return "预测天气：{}，{}，{}，{}，{}{}级".format(
                    data.get('daily_forecast')[0].get('date'),
                    data.get('basic').get('location'),
                    data.get('daily_forecast')[0].get('cond_txt_d'),
                    "{}-{}℃".format(data.get('daily_forecast')[0].get('tmp_min'),
                                    data.get('daily_forecast')[0].get('tmp_max')),
                    data.get('daily_forecast')[0].get('wind_dir'),
                    data.get('daily_forecast')[0].get('wind_sc')
                )
            elif weather_type == 'lifestyle':
                types = {
                    "comf": "舒适度指数",
                    # "drsg": "穿衣指数",
                    # "flu": "感冒指数",
                    # "air": "空气指数",
                    # "spi": "防晒指数"
                }
                base_str =  ""
                for br in data.get('lifestyle'):
                    if br.get('type') in types.keys():
                        base_str += "{}: {}\n".format(types.get(br.get('type')), br.get('txt'))
                return base_str
