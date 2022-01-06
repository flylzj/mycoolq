# coding: utf-8
import aiohttp


class BaseSign:
    pass


class T00lsSign(BaseSign):
    login_url = "https://www.t00ls.cc/login.json"
    sign_url = "https://www.t00ls.cc/ajax-sign.json"

    def __init__(self, username, login_form):
        self.username = username
        self.login_form = login_form
        self.reason = "签到成功"

    async def login(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.login_url, data=self.login_form) as resp:
                resp_json: dict = await resp.json()
                if resp_json.get("status") != "success":
                    self.reason = f'登录失败：{resp_json.get("message")}'
                return resp_json.get("formhash"), resp.cookies

    async def sign(self, formhash, cookies):
        sign_data = {
            'formhash': formhash,
            'signsubmit': "true"
        }
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.post(self.sign_url, data=sign_data) as resp:
                resp_json: dict = await resp.json()
                if resp_json.get("status") != "success":
                    self.reason = f'签到失败：{resp_json.get("message")}'
                return resp_json.get("status") == "success"

    async def login_and_sign(self):
        formhash, cookies = await self.login()
        if not formhash:
            return False, self.reason
        status = await self.sign(formhash, cookies)
        return status, self.reason
