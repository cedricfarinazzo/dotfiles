import subprocess

from i3status import Task, TaskInsert
from .utils import color_get, BLK

MIN_TEMP = 19
MAX_TEMP = 110

def get_temp():
    try:
        p = subprocess.run(['sensors'], stdout=subprocess.PIPE)
        if p.returncode != 0:
            raise Exception
        output = p.stdout.decode()
        cpu_temp = output[output.index("Package id 0: "):
                          output.index("(high = +100.0")]
        cpu_temp = cpu_temp.split(':')[1]
        cpu_temp = cpu_temp.split(' ')
        cpu_temp = ''.join(cpu_temp)
        temp = float(cpu_temp[1:cpu_temp.index("°C")])

        return cpu_temp, color_get(temp, MIN_TEMP, MAX_TEMP)
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
