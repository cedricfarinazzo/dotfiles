import re
import subprocess

from i3status import Task, TaskInsert
from .utils import color_get, BLK

MIN_TEMP = 19
MAX_TEMP = 110

regex = re.compile('.*:\s*(\+(\d+\.\d+)°C)')

def get_temp():
    try:
        p = subprocess.run(['sensors'], stdout=subprocess.PIPE)
        if p.returncode != 0:
            raise Exception

        output = p.stdout.decode().strip().split('\n')
        if len(output) < 3:
            raise Exception

        result = regex.match(output[2])
        if not result:
            raise Exception


        return result.group(1), color_get(float(result.group(2)), MIN_TEMP, MAX_TEMP)
    except Exception:
        return "ERROR", BLK

def temp():
    temp, t_color = get_temp()
    return {
            'name': 'temperatur',
            'markup': 'none',
            'color': t_color,
            'full_text': temp
           }

Task.register(TaskInsert(8, temp))
