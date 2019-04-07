# coding: utf-8
from nonebot import on_command, CommandSession
import aiohttp, asyncio
from config import MOVIE_URL
from bs4 import BeautifulSoup
import re


@on_command('movie', aliases=('我想看', ))
async def movie_command(session: CommandSession):
    movie = session.get('movie', prompt="你想看什么")

    movie_link = await get_movie(movie)

    await session.send(movie_link)


@movie_command.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['movie'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg


async def get_movie(movie: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(MOVIE_URL + "?s={}".format(movie), allow_redirects=True) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            movies = []
            for m in soup.find_all('article', attrs={"itemtype": "http://schema.org/BlogPosting"}):
                async with session.get(m.find('h2', attrs={"class": "entry-title"}).a['href']) as link_r:
                    link_soup = BeautifulSoup(await link_r.text(), 'html.parser')
                    pans = link_soup.find_all('a', attrs={"href": re.compile(r'https://pan.baidu.com/s/.*')})
                    if pans:
                        movies.append(
                            m.find('h2', attrs={"class": "entry-title"}).text + "\n".join(
                                [
                                    pan['href'] + pan.parent.text
                                    for pan in pans
                                ]
                            ) + "\n" + "-" * 30
                        )
            if not movies:
                return "没有找到"
            return "".join(movies)

