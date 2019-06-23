import datetime as dt
import time


def get_today_datetime(timezone=8):
    now = dt.datetime.utcnow() + dt.timedelta(hours=timezone)
    today = dt.datetime(year=now.year, month=now.month, day=now.day)
    return today


def get_today_eight_oclock_datetime(timezone=8):
    return get_today_datetime(timezone=timezone) + dt.timedelta(hours=8)


def get_today_eight_oclock_unixtime(timezone=8):
    t = get_today_datetime(timezone=timezone) + dt.timedelta(hours=8)
    return int(time.mktime(t.timetuple()))

def get_today_unixtime(timezone=8):
    return int(time.mktime(get_today_datetime(timezone).timetuple()))


def get_now_datatime(timezone=8):
    now = dt.datetime.utcnow()
    return now + dt.timedelta(hours=timezone)
