import datetime as dt
import time


def get_today_datetime(timezone=8):
    now = dt.datetime.utcnow() + dt.timedelta(hours=timezone)
    today = dt.datetime(year=now.year, month=now.month, day=now.day)
    return today


def get_today_unixtime(timezone=8):
    return int(time.mktime(get_today_datetime(timezone).timetuple()))


def get_now_datatime(timezone=8):
    now = dt.datetime.utcnow()
    return now + dt.timedelta(hours=timezone)
