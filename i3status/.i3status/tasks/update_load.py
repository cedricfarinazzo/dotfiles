import re
from i3status import Task, TaskUpdate
from .utils import color_get

MIN_LOAD = 0
MAX_LOAD = 10

regex = re.compile('.*load\s*(\d+,\d+)')


def update_load(loadjson):
    result = regex.match(loadjson['full_text'])
    if not result:
        return
    value = float(result.group(1).replace(',', '.'))

    loadjson['color'] = color_get(value, MIN_LOAD, MAX_LOAD)

Task.register(TaskUpdate(2, update_load))
