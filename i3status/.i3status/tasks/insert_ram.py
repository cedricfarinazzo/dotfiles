import subprocess

from i3status import Task, TaskInsert
from .utils import color_get, BLK

MIN_RAM = 0
MAX_RAM = 100

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
        output = p.stdout.decode()
        stat = output.split('\n')[-2].split(' ')
        stat = [e for e in stat if e != ''][1:]

        tot_m, used_m, _ = map(int, stat)
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
