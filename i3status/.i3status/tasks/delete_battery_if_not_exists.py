from i3status import Task, TaskDeleteIf

def delete_battery_if_not_exists(batjson):
    return "No battery" in batjson['full_text']

Task.register(TaskDeleteIf(7, delete_battery_if_not_exists))
