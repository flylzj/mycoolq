# coding: utf-8
import aiohttp
from bs4 import BeautifulSoup
import asyncio
import random


async def get_sentence(word: str) -> str:
    api = "http://zaojv.com/wordQueryDo.php"
    pass
    async with aiohttp.ClientSession() as session:
        data = {
            "nsid": 0,
            "s": "4595742426291063331",
            "q": "",
            "wo": word,
            "directGo": 1
        }
        async with session.post(api, data=data) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            all = soup.find("div", attrs={"id": "all"})
            try:
                sentence = random.choice(all.find_all("div", recursive=False))
                s = ""
                for i in sentence.text:
                    if i.isdigit():
                        print(i)
                        continue
                    s += i
                return s.strip()
            except Exception as e:
                return ""


if __name__ == '__main__':
    word = "一笑而过"
    loop = asyncio.get_event_loop()
    tasks = [get_sentence(word)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()