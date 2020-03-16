from i3status import Task, TaskUpdate
from .utils import color_get

MAX_LEN_WIRELESS_NAME = 7

def minimize_wireless_msg(json):
    try:
        text = json['full_text']

        if "no wlan" in text:
            return

        pre = text[:text.index('at ') + 3]
        mid = text[text.index('at ') + 3 : text.index(', ')]
        end = text[text.index(', '):]

        if len(mid) > MAX_LEN_WIRELESS_NAME:
            mid = mid[:MAX_LEN_WIRELESS_NAME] + '..'

        json['full_text'] = pre + mid + end
    except Exception:
        pass

Task.register(TaskUpdate(4, minimize_wireless_msg))
