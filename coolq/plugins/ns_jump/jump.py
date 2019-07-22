# coding: utf-8
import aiohttp

JUMP_SEARCH_API = "https://switch.vgjump.com/switch/gameDlc/list?title={}&offset=0&limit=10"
JUMP_GAME_API = "https://switch.vgjump.com/switch/gameInfo?appid={}&" \
                "system=Android%208.0.0&platform=android&fromName=search"


async def search_game(title: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(JUMP_SEARCH_API.format(title)) as r:
            return parse_res(await r.json())
            # return parse_res(await r.json())


def parse_res(data: dict) -> str:
    if data.get("result").get("code") != 0:
        return ""
    else:
        games = data.get("data").get("games")
        if not games:
            return ""
        res = ""
        for game in games:
            res += "游戏名:{}\nappid：{}\n原价:{}\n现价:{}\n".format(
                str(game.get("titleZh")),  # + str(game.get("title")),  # 这里的名字可能会为None
                game.get("appid"),
                game.get("priceRaw") if game.get("priceRaw") else "暂无",
                game.get("price") if game.get("price") else "暂无"
            )
        return res


async def get_game_detail(appid: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(JUMP_GAME_API.format(appid)) as r:
            return parse_game_res(await r.json())


def parse_game_res(data: dict) -> str:
    if data.get("result").get("code") != 0:
        return ""
    data = data.get("data")
    res = "游戏名：{}\n评价：{}\n玩家人数：{}\n".format(
        data.get("game").get("titleZh"),
        data.get("game").get("recommendLabel") if data.get("game").get("recommendLabel") else "暂无评价",
        "{}-{}人".format(data.get("game").get("playersMin"), data.get("game").get("players"))
    )
    prices = data.get("prices")
    prices.sort(key=lambda p: float(p.get("price")) if p.get("price") else 1)
    for p in prices[:3]:
        res += "{}区价格：￥{}".format(p.get("country"), p.get("price"))
        if p.get("leftDiscount"):
            res += "(优惠剩余{})\n".format(p.get("leftDiscount"))
        else:
            res += "\n"
    return res


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    tasks = [search_game("杀戮")]
    loop.run_until_complete(asyncio.wait(tasks))