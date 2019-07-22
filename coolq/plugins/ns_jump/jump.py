# coding: utf-8
import aiohttp

JUMP_SEARCH_API = "https://switch.vgjump.com/switch/gameDlc/list?title={}&offset=0&limit=10"


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
            res += "游戏名:{}\n原价:{}\n现价:{}\n".format(
                str(game.get("titleZh")) + str(game.get("title")),  # 这里的名字可能会为None
                game.get("priceRaw") if game.get("priceRaw") else game.get("price"),
                game.get("price")
            )
        return res


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    tasks = [search_game("杀戮")]
    loop.run_until_complete(asyncio.wait(tasks))