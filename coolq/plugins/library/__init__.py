# coding: utf-8
from nonebot import on_command, CommandSession
import asyncio
from nonebot import logger
import aiohttp
import json
import re
import queue


@on_command('library', aliases=('图书馆', ))
async def movie_command(session: CommandSession):
    book = session.get('library', prompt="请输入参数")

    movie_link = await get_books(book=book)

    await session.send(movie_link)

@movie_command.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['library'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的关键词不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg

async def get_books(book: str) -> str:
    logger.info(book)
    book_search_url = "http://210.35.251.243/opac/ajax_search_adv.php"
    async with aiohttp.ClientSession() as session:
        data = {
            "filters": [],
            "first": True,
            "limiter": [],
            "locale": "zh_CN",
            "pageCount": 1,
            "pageSize": 20,
            "searchWords": [
                {
                    "fieldList": [
                        {
                            "fieldCode": "",
                            "fieldValue": book
                        }
                    ]
                }
            ],
            "sortField": "relevance",
            "sortType": "desc"
        }
        async with session.post(book_search_url, json=data) as res:
            data = json.loads(await res.text())
            contents = data.get("content")
            res = "{:10}{:10}{:10}\n".format("书名", "作者", "数量")
            for book in contents:
                count = await get_book_num(book)
                res += "{:10}{:10}{:10}\n".format(book.get("title"), book.get("author"), count)
            return res




async def get_book_num(book_info):
    url = "http://210.35.251.243/opac/ajax_isbn_marc_no.php?marc_no={}&rdm=0.3894705377335508&isbn={}".format(
        book_info.get("marcRecNo"), book_info.get("marcRecNo")
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            data = json.loads(await res.text())
            return re.sub(r'<.*>', "", data.get("lendAvl"))


def parse_books(data):
    contents = data.get("content")
    res = "{}\t{}\t{}\n".format("书名", "作者", "剩余数量")
    for book in contents:
        res += "{}\t{}\t{}\n".format(book.get("title"), book.get("author"), book.get("num"))
    return res



