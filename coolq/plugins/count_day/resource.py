# coding: utf-8
from coolq.db.models import Days


def to_zero(user_id):
    Days.to_zero(user_id)


def increase_one(user_id):
    Days.increase_one(user_id)


def get_need_increase():
    for d in Days.get_need_increase():
        yield d