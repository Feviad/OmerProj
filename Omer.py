from datetime import datetime, timedelta
import pytz
import requests


URL = 'http://db.ou.org/zmanim/getCalendarData.php'


def get_user_sunset(tz, loc) -> datetime.time:
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    date_str = f'{now.month}/{now.day}/{now.year}'
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': date_str,
        'lat': loc[0],
        'lng': loc[1]
    }
    zmanim = requests.get(URL, params=params)
    zmanim_dict = zmanim.json()
    zmanim_dict = zmanim_dict['zmanim']
    timer = datetime.strptime(zmanim_dict['sunset'], "%H:%M:%S")
    delta = timedelta(hours=1)
    timer = datetime.time(timer - delta)
    return timer


print(get_user_sunset("Europe/Moscow", (35.33,50.333)))
