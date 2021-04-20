# coding: utf-8
import json
from coolq.db.models import SignInAccount, SignInAccountEnum
from .t00ls import T00ls


class SignInResource(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def t00ls_account_add(self, username, password, questionid="0", answer=""):
        account_type = SignInAccountEnum.t00ls_account.int_value
        account_info = json.dumps(
            {
                "username": username,
                "password": password,
                "questionid": questionid,
                "answer": answer
            }
        )
        account_id = SignInAccount.insert_account(user_id=self.user_id, account_type=account_type, account_info=account_info)
        if account_id:
            return f"账号添加成功，id：{account_id}"
        else:
            return f"账号添加失败"

    def t00ls_account_update(self, account_id, **data):
        res = SignInAccount.update_account(self.user_id, account_id, **data)
        if res:
            return f"账号更新成功"
        else:
            return f"账号更新失败"

    def get_t00ls_account(self):
        message = "账号列表如下\nid\tusername\n"
        for r in SignInAccount.get_accounts(SignInAccountEnum.t00ls_account.int_value, user_id=self.user_id):
            message += f"{r.id}\t{json.loads(r.account_info).get('username')}"
        return message

    @staticmethod
    def get_all_t00ls_account():
        for r in SignInAccount.get_accounts(SignInAccountEnum.t00ls_account.int_value):
            yield r

    @staticmethod
    async def t00ls_sign_in(account_info):
        t00ls = T00ls(**account_info)
        return await t00ls.login_and_check_in()
