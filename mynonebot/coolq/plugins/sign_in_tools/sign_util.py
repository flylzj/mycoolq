# coding: utf-8
import aiohttp
from nonebot.log import logger


class BaseSign:
    pass


class T00lsSign(BaseSign):
    login_url = "https://www.t00ls.cc/login.json"
    sign_url = "https://www.t00ls.cc/ajax-sign.json"
    profile_url = "https://www.t00ls.net/members-profile.json"

    SUCCESS = "success"

    message_temp = "土司签到{}\n当前tubi：{}\n银行存款：{}\nreason\n{}"

    TUBI_KEY = "extcredits2"  # tubi数量
    TUBE_STORE_KEY = "extcredits3"  # 存款数量

    def __init__(self, username, login_form):
        self.username = username
        self.login_form = login_form
        self.reason = ""
        self.cookies = None
        self.formhash = ""

    async def login(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.login_url, data=self.login_form) as resp:
                resp_json: dict = await resp.json()
                logger.debug("login resp ")
                logger.debug(resp_json)
                if resp_json.get("status") != self.SUCCESS:
                    self.reason += f'登录失败：{resp_json.get("message")}'
                    return
                logger.debug("登录成功")
                self.cookies = resp.cookies
                self.formhash = resp_json.get("formhash")

    async def _sign(self):
        sign_data = {
            'formhash': self.formhash,
            'signsubmit': "true"
        }
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.post(self.sign_url, data=sign_data) as resp:
                resp_json: dict = await resp.json()
                if resp_json.get("status") != self.SUCCESS:
                    self.reason += f'签到失败：{resp_json.get("message")}'
                return resp_json.get("status") == self.SUCCESS

    async def _get_profile(self):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(self.profile_url) as resp:
                resp_json: dict = await resp.json()
                if resp_json.get("status") != self.SUCCESS:
                    self.reason += f"获取profile失败：{resp_json.get('message')}"
                    return {}
                return resp_json.get("memberinfo")

    async def sign_and_get_profile(self):
        await self.login()
        if not self.formhash or not self.cookies:
            return self.message_temp.format(
                "失败",
                0,
                0,
                self.reason
            )
        sign_status = await self._sign()
        profile = await self._get_profile()
        tubi_count = profile.get(self.TUBI_KEY)
        tubi_store_count = profile.get(self.TUBE_STORE_KEY)

        return self.message_temp.format(
            "成功" if sign_status else "失败",
            tubi_count,
            tubi_store_count,
            self.reason
        )







