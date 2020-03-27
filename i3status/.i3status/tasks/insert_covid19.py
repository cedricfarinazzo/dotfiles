import os
import re
import urllib
import urllib.request
import time
import subprocess

from i3status import Task, TaskInsert
from .utils import color_get, BLK, RED

COVID19_CACHE_PATH = '/tmp/.i3status_covid19.dat'
COVID19_API_URL = 'https://www.worldometers.info/coronavirus'

def launch_covid19_scrapper():
    def child():
        user_agent = "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/74.0"
        headers = {'User-Agent': user_agent}
        while True:
            try:
                req = urllib.request.Request(COVID19_API_URL, headers=headers)
                with urllib.request.urlopen(req) as response:
                    html = response.read().decode('utf-8')
                    m = re.search(r'<title>Coronavirus Update \(Live\):\s+(\d+,\d+)\s+Cases', html)
                    with open(COVID19_CACHE_PATH, "w+") as handler:
                        handler.write(m.group(1))
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
        return "Covid19: " + nb, RED
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
