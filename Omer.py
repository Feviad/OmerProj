import psycopg2
from datetime import datetime, timedelta
import pytz, requests


URL = 'http://db.ou.org/zmanim/getCalendarData.php'

def get_location_by_id(user_id: int) -> tuple:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT latitude, longitude FROM locations ' \
                f'WHERE id = {user_id}'
        cur.execute(query)
        location = cur.fetchone()
        response = location
        return response


def get_tz_by_id(user_id: int) -> str:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT public.tz.tz FROM public.tz WHERE id = {user_id}'
        cur.execute(query)
        tz = cur.fetchone()
        response = tz[0]
        return response


def get_user_sunset(user_id: int) -> datetime.time:
    tz = get_tz_by_id(user_id)
    loc = get_location_by_id(user_id)
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