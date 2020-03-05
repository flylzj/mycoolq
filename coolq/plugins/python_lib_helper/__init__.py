# coding: utf-8
from nonebot import on_command, CommandSession
import nonebot
import aiohttp
from bs4 import BeautifulSoup
from coolq.db.model.python_lib_helper import insert_lib, find_lib, insert_lang_ref, find_lang_ref
from config import LIB_URL, LIB_ROOT_URL, THIRD_LIB_ROOT_URL, PYTHON_TUTORIALS_URL, LOCAL_LIB_URL,\
    LANG_REF_URL, LANG_REF_ROOT_URL, LOCAL_LANG_REF_ROOT_URL,\
    DOC_ROOT_URL, LOCAL_DOC_ROOT_URL


@on_command('lib', aliases=('标准库',), only_to_me=False)
async def lib_command(session: CommandSession):
    lib_name = session.get_optional('lib')
    if not lib_name:
        message = "标准库链接:\n镜像链接:{}\n官方链接:{}".format(LOCAL_LIB_URL, LIB_URL)
        await session.send(message)
        return
    lib = find_lib(lib_name)
    if lib:
        message = "{}链接：{}".format(lib.comment, lib.url.replace(DOC_ROOT_URL, LOCAL_DOC_ROOT_URL))
        await session.send(message)
    else:
        # message = await spider_third_lib(lib_name)
        message = "{}未找到".format(lib_name if lib_name else "")
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


@on_command('lang', aliases=('语言参考',), only_to_me=False)
async def lang_command(session: CommandSession):
    lang_ref_name = session.get_optional('lang')
    if not lang_ref_name:
        message = "语言参考:\n镜像链接:{}\n官方链接:{}".format(LOCAL_LANG_REF_ROOT_URL, LANG_REF_URL)
        await session.send(message)
        return

    lang_ref = find_lang_ref(many=True, title1=lang_ref_name)
    if lang_ref:
        href = lang_ref[0].url.split('#')[0].replace(DOC_ROOT_URL, LOCAL_DOC_ROOT_URL)
        message = f"{lang_ref[0].title1}---{href}\n{','.join([lang.title2 for lang in lang_ref])}"
        await session.send(message)
    else:
        message = "未找到"
        await session.send(message)



@lang_command.args_parser
async def lang_command_parser(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['lang'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请输入正确的title')
    session.state[session.current_key] = stripped_arg


@nonebot.scheduler.scheduled_job('cron', minute="0-59/1")
async def spider_lib():
    async for lib in spider_standard_lib():
        insert_lib(**lib)

    async for lang in spider_lang_ref():
        insert_lang_ref(**lang)


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

async def spider_lang_ref():
    async with aiohttp.ClientSession() as session:
        async with session.get(LANG_REF_URL) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            title1s = soup.find_all('li', attrs={'class': 'toctree-l1'})
            for title1 in title1s:
                title1_text = title1.a.text.split('.')[-1].strip()
                title2s = title1.find_all('li', attrs={'class': 'toctree-l2'})
                for title2 in title2s:
                    title2_text = title2.a.text.split('.')[-1].strip()
                    href = LANG_REF_ROOT_URL + title2.a['href']
                    yield {
                        'title1': title1_text,
                        'title2': title2_text,
                        'url': href
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
    loop.run_until_complete(spider_lang_ref())
