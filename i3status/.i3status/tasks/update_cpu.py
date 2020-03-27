from i3status import Task, TaskUpdate
from .utils import color_get

MIN_CPU = 0
MAX_CPU = 100

def update_cpu(cpujson):
    text = cpujson['full_text']
    value = text[text.index('u ') + 1:text.index('%')].split(' ')
    value = int(''.join(value))

    cpujson['color'] = color_get(value, MIN_CPU, MAX_CPU)

Task.register(TaskUpdate(0, update_cpu))
