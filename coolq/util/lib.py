# coding: utf-8
from datetime import datetime
import time


def get_today_start_end():
    today_start = time.mktime(datetime.today().date().timetuple())
    today_end = today_start + 86400
    return today_start, today_end
