from i3status import Task, TaskUpdate
from .utils import color_get

MIN_LOAD = 0
MAX_LOAD = 10

def update_load(loadjson):
    text = loadjson['full_text']
    text = text.replace('load ', '')
    text = ''.join(text.split(' '))
    text = text.replace(',', '.')

    loadjson['color'] = color_get(float(text), MIN_LOAD, MAX_LOAD)

Task.register(TaskUpdate(2, update_load))
