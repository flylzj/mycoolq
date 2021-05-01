# coding: utf-8
import aiohttp
from nonebot.log import logger


class T00ls:
    login_questions = '''
    # 0 = 没有安全提问
    # 1 = 母亲的名字
    # 2 = 爷爷的名字
    # 3 = 父亲出生的城市
    # 4 = 您其中一位老师的名字
    # 5 = 您个人计算机的型号
    # 6 = 您最喜欢的餐馆名称
    # 7 = 驾驶执照的最后四位数字
    '''
    login_url = "https://www.t00ls.net/login.json"
    check_in_url = "https://www.t00ls.net/ajax-sign.json"

    def __init__(self, username, password, questionid, answer):
        self.login_data = {
            "action": "login",
            "username": username,
            "password": password,
            "questionid": questionid,
            "answer": answer
        }
        self.cookies = None

    async def t00ls_login(self, session: aiohttp.ClientSession):
        try:
            async with session.post(self.login_url, data=self.login_data) as response:
                data = await response.json()
                print(data)
                if data.get("status") == "success":
                    return data.get("formhash")
        except Exception as e:
            logger.error(f"t00ls_login err {str(e)}")

    async def t00ls_check_in(self, session: aiohttp.ClientSession, formhash):
        sign_data = {
            "formhash": formhash,
            "signsubmit": "true"
        }
        try:
            async with session.post(self.check_in_url, data=sign_data, cookies=self.cookies) as response:
                data = await response.json()
                print(data)
                if data.get("status") == "success":
                    return True
        except Exception as e:
            logger.error(f"t00ls_check_in err {str(e)}")

    async def login_and_check_in(self):
        async with aiohttp.ClientSession() as session:
            formhash = await self.t00ls_login(session)
            if not formhash:
                logger.error("login_and_check_in err formhash is empty")
                return False
            return await self.t00ls_check_in(session, formhash)


if __name__ == '__main__':
    import asyncio
    login_data = {
        'username': '',
        'password': '',
        'questionid': '',
        'answer': ''
    }
    t00ls = T00ls(**login_data)
    asyncio.run(t00ls.login_and_check_in())