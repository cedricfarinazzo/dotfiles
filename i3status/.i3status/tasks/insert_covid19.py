import os
import subprocess

from i3status import Task, TaskInsert
from .utils import color_get, BLK

COVID19_CACHE_PATH = '/tmp/.i3status_covid19.dat'
COVID19_API_URL = 'https://coronavirus-tracker-api.herokuapp.com/confirmed'

def launch_covid19_scrapper():
    def child():
        while True:
            try:
                data = urllib.request.urlopen(COVID19_API_URL).read().decode('utf-8')
                j = json.loads(data)
                with open(COVID19_CACHE_PATH, "w+") as handler:
                    handler.write(str(j['latest']))
            except:
                pass
            time.sleep(60 * 5) # 5 min

    pid = os.fork()
    if pid == 0:
        child()

launch_covid19_scrapper()

def get_covid19_data():
    try:
        with open(COVID19_CACHE_PATH, "r") as handler:
            nb = handler.read()
        return "Covid19: " + nb
    except Exception:
        return "Covid19: NO DATA", BLK

def covid19_data():
    nb, color = get_covid19_data()
    return {
            'name': 'covid19',
            'markup': 'none',
            'color': color,
            'full_text': nb
           }

Task.register(TaskInsert(9, covid19_data))
