import re
from i3status import Task, TaskUpdate
from .utils import color_get

MIN_CPU = 0
MAX_CPU = 100

regex = re.compile('.*cpu\s*(\d+)%')

def update_cpu(cpujson):
    result = regex.match(cpujson['full_text'])
    if not result:
        return

    value = int(result.group(1))

    cpujson['color'] = color_get(value, MIN_CPU, MAX_CPU)

Task.register(TaskUpdate(0, update_cpu))
