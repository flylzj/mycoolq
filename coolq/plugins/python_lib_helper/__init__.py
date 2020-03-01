# coding: utf-8
from nonebot import on_command, CommandSession
import nonebot
import aiohttp
from bs4 import BeautifulSoup
from coolq.db.model.python_lib_helper import insert_lib, find_lib
from config import LIB_URL, LIB_ROOT_URL

@on_command('lib', aliases=('标准库',), only_to_me=False)
async def lib_command(session: CommandSession):
    lib_name = session.get('lib', prompt='标准库未找到')
    lib = find_lib(lib_name)
    if lib:
        message = "{}链接：{}".format(lib.comment, lib.url)
        await session.send(message)
    else:
        message = "未找到 {}".format(lib_name)
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


@nonebot.scheduler.scheduled_job('cron', minute="0-59/1")
async def spider_lib():
    async for lib in spider():
        insert_lib(**lib)


async def spider():
    async with aiohttp.ClientSession() as session:
        async with session.get(LIB_URL) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            libs = soup.find_all('li', attrs={'class': 'toctree-l2'})
            data = []
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



if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider())
