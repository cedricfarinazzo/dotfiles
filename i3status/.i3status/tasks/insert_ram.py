import subprocess
import re

from i3status import Task, TaskInsert
from .utils import color_get, BLK

MIN_RAM = 0
MAX_RAM = 100

regex = re.compile('Total:\s*(\d+)\s+(\d+)')

def normalize_ram(ram):
    if ram <= 999:
        return str(ram) + "Mib"
    else:
        ram = round(ram / 1000, 1)
        return str(ram) + "Gib"


def get_ram_usage():
    try:
        p = subprocess.run(['free', '-t', '-m'], stdout=subprocess.PIPE)
        if p.returncode != 0:
            raise Exception

        result = regex.match(p.stdout.decode().strip().split('\n')[-1])
        if not result:
            raise Exception

        tot_m, used_m = int(result.group(1)), int(result.group(2))
        usage = int(used_m * 100 / tot_m)

        ram = "%d%%(%s / %s)" % (usage, normalize_ram(used_m),
                                 normalize_ram(tot_m))
        return ram, color_get(usage, MIN_RAM, MAX_RAM)
    except Exception:
        return "ERROR", BLK

def ram_usage():
    ram, r_color = get_ram_usage()
    return {
            'name': 'ram',
            'markup': 'none',
            'color': r_color,
            'full_text': ram
           }

Task.register(TaskInsert(1, ram_usage))
