#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script is a simple wrapper which prefixes each i3status line with custom
# information. It is a python reimplementation of:
# http://code.stapelberg.de/git/i3status/tree/contrib/wrapper.pl
#
# To use it, ensure your ~/.i3status.conf contains this line:
#     output_format = "i3bar"
# in the 'general' section.
# Then, in your ~/.i3/config, use:
#     status_command i3status | ~/i3status/contrib/wrapper.py
# In the 'bar' section.
#
# In its current version it will display the cpu frequency governor, but you
# are free to change it to display whatever you like, see the comment in the
# source code below.

# © 2012 Valentin Haenel <valentin.haenel@gmx.de>
#
# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law. You can redistribute it and/or modify it under
# the terms of the Do What The Fuck You Want To Public License (WTFPL), Version
# 2, as published by Sam Hocevar. See http://sam.zoy.org/wtfpl/COPYING for more
# details.

import sys
import os
import pickle
import subprocess
import json

# Colors

WHT = "#FFFFFF"
BLK = "#000000"
RED = "#FF0011"
ORG = "#FF6100"
YLW = "#E3FF00"
GRN = "#00FF46"

COLOR_CACHE_PATH = '/tmp/.i3status_color.dat'
COLOR_STEP = 5
COLOR = []
NBCOLOR = 0


def color_generate(step=1):
    color = list()
    r, g = 0, 255
    while r <= 255:
        color.append('#%X%X00' % (r, 255))
        r += step

    g = 255
    while g >= 0:
        color.append('#%X%X00' % (255, g))
        g -= step

    return color


def color_init():
    global COLOR
    global NBCOLOR
    try:
        with open(COLOR_CACHE_PATH, "rb") as file:
            COLOR = pickle.load(file)
    except Exception:
        COLOR = color_generate(COLOR_STEP)
        with open(COLOR_CACHE_PATH, "wb") as file:
            pickle.dump(COLOR, file)
    NBCOLOR = len(COLOR)


def color_get(val, mini, maxi):
    step = (maxi - mini) / NBCOLOR
    color_id = int((val - MIN_LOAD) / step)
    return COLOR[color_id if color_id < NBCOLOR else -1]


# CONFIG

STEP = 5

MIN_CPU = -5
MAX_CPU = 106

MIN_RAM = -2
MAX_RAM = 106

MIN_TEMP = 19
MAX_TEMP = 80

MIN_LOAD = 0
MAX_LOAD = 5

MAX_LEN_WIRELESS_NAME = 7

# FUNCTION


def get_governor():
    """ Get the current governor for cpu0, assuming all CPUs use the same. """
    with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor') as fp:
        return fp.readlines()[0].strip()


def get_wireless_json_part(json):
    for e in json:
        try:
            if e['name'] == 'wireless':
                return e
        except Exception:
            pass
    return None


def minimize_wireless_msg(json):
    try:
        text = json['full_text']

        if "  no wlan  " in text or "  no wlan  " == text:
            return

        pre = text[:text.index('at ')+3]
        mid = text[text.index('at ')+3:text.index(', ')]
        end = text[text.index(', '):]

        if len(mid) > MAX_LEN_WIRELESS_NAME:
            mid = mid[:MAX_LEN_WIRELESS_NAME] + '..'

        json['full_text'] = pre + mid + end
    except Exception:
        pass


def update_cpu(cpujson):
    text = cpujson['full_text']
    value = text[text.index('u ')+1:text.index('%')].split(' ')
    value = int(''.join(value))

    try:
        cpujson.pop('color')
    except Exception:
        pass

    color = COLOR[0]
    step = (MAX_CPU - MIN_CPU) / NBCOLOR
    for i in range(NBCOLOR):
        u = (i * step) + MIN_CPU
        if value < u:
            color = COLOR[i]
            break
    cpujson['color'] = color


def update_load(loadjson):
    text = loadjson['full_text']
    text = text.replace('load ', '')
    text = ''.join(text.split(' '))
    text = text.replace(',', '.')
    value = float(text)

    try:
        loadjson.pop('color')
    except Exception:
        pass

    color = COLOR[0]
    step = (MAX_LOAD - MIN_LOAD) / NBCOLOR
    for i in range(NBCOLOR):
        u = (i * step) + MIN_LOAD
        if value < u:
            color = COLOR[i]
            break
    loadjson['color'] = color


def get_temp():
    p = subprocess.Popen("sensors", stdout=subprocess.PIPE, shell=False)
    (output, err) = p.communicate()
    p_status = p.wait()
    if p_status != 0:
        return "ERROR", BLK
    output = output.decode("utf-8")

    try:
        cpu_temp = output[output.index("Package id 0: "):
                          output.index("(high = +100.0")]
        cpu_temp = cpu_temp.split(':')[1]
        cpu_temp = cpu_temp.split(' ')
        cpu_temp = ''.join(cpu_temp)

        temp = float(cpu_temp[1:cpu_temp.index("°C")])

        color = COLOR[0]
        step = (MAX_TEMP - MIN_TEMP) / NBCOLOR
        for i in range(NBCOLOR):
            u = (i * step) + MIN_TEMP
            if temp < u:
                color = COLOR[i]
                break
        return cpu_temp, color
    except Exception:
        return "ERROR", BLK


def normalize_ram(ram):
    if (ram <= 999):
        return str(ram) + "Mib"
    else:
        ram = round(ram/1000, 1)
        return str(ram) + "Gib"


def get_ram_usage():
    tot_m, used_m, free_m = \
        map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    usage = int(((used_m/tot_m)*100))
    ram = " " + str(usage) + "% (" + \
          normalize_ram(used_m) + " / " + normalize_ram(tot_m) + ") "
    color = COLOR[0]
    step = (MAX_RAM - MIN_RAM) / NBCOLOR
    for i in range(NBCOLOR):
        u = (i * step) + MIN_RAM
        if usage < u:
            color = COLOR[i]
            break
    return ram, color


# WRAPPER

def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()


def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    color_init()

    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        if line.startswith(','):
            line, prefix = line[1:], ','

        j = json.loads(line)
        # insert information into the start of the json, but could be anywhere
        # CHANGE THIS LINE TO INSERT SOMETHING ELSE

        # RAM
        (ram, r_color) = get_ram_usage()
        j.insert(1,
                 {
                     'name': 'ram',
                     'markup': 'none',
                     'color': r_color,
                     'full_text': '%s' % ram
                 })

        # TEMP
        (temp, t_color) = get_temp()
        j.insert(8,
                 {
                     'name': 'temperatur',
                     'markup': 'none',
                     'color': t_color,
                     'full_text': '%s' % temp
                 })

        # CPU
        update_cpu(j[0])

        # LOAD
        update_load(j[2])

        # WIRELESS
        wireless = get_wireless_json_part(j)
        minimize_wireless_msg(wireless)

        # and echo back new encoded json
        print_line(prefix+json.dumps(j))
