# coding: utf-8
from nonebot import on_command, CommandSession
import nonebot
import aiohttp
from bs4 import BeautifulSoup
from coolq.db.model.python_lib_helper import insert_lib, find_lib
from config import LIB_URL, LIB_ROOT_URL, THIRD_LIB_ROOT_URL, PYTHON_TUTORIALS_URL


@on_command('lib', aliases=('标准库',), only_to_me=False)
async def lib_command(session: CommandSession):
    lib_name = session.get('lib', prompt='标准库未找到')
    lib = find_lib(lib_name)
    if lib:
        message = "{}链接：{}".format(lib.comment, lib.url)
        await session.send(message)
    else:
        # message = await spider_third_lib(lib_name)
        message = "{}未找到".format(lib_name)
        await session.send(message)


@lib_command.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['lib'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请输入正确的标准库名称')
    session.state[session.current_key] = stripped_arg


@nonebot.scheduler.scheduled_job('cron', day="1-31/1")
async def spider_lib():
    async for lib in spider_standard_lib():
        insert_lib(**lib)


async def spider_standard_lib():
    async with aiohttp.ClientSession() as session:
        async with session.get(LIB_URL) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            libs = soup.find_all('li', attrs={'class': 'toctree-l2'})
            for lib in libs:
                name_tag = lib.find('code', attrs={'class': 'xref py py-mod docutils literal notranslate'})
                # not a module
                if not name_tag:
                    continue
                title = lib.parent.parent.find(text=True)
                name = name_tag.text
                comment = lib.a.text
                url = LIB_ROOT_URL + lib.a['href']
                yield {
                    "title": title,
                    "name": name,
                    "comment": comment,
                    "url": url
                }


async def spider_third_lib(lib_name) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(THIRD_LIB_ROOT_URL + lib_name + "/") as r:
            if r.status != 200:
                return "未找到{}的文档".format(lib_name)
            try:
                soup = BeautifulSoup(await r.text(), 'html.parser')
                doc_tag = soup.find("i", attrs={"class": "fas fa-book"})
                doc_href = ""
                if doc_tag:
                    doc_href = doc_tag.parent['href']
                return "{}文档地址：{}".format(lib_name, doc_href)
            except Exception as e:
                return str(e)


@on_command('tutorials', aliases=('教程传送门',), only_to_me=False)
async def tutorials(session: CommandSession):
    message = "教程来啦：{}".format(PYTHON_TUTORIALS_URL)
    await session.send(message)


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider_third_lib("testasdasd"))
