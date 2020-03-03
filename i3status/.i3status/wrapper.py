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

import os
import sys
import urllib
import urllib.request
import time
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

COVID19_CACHE_PATH = '/tmp/.i3status_covid19.dat'
COVID19_API_URL = 'https://coronavirus-tracker-api.herokuapp.com/confirmed'
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

MIN_CPU = 0
MAX_CPU = 100

MIN_RAM = 0
MAX_RAM = 100

MIN_TEMP = 19
MAX_TEMP = 110

MIN_LOAD = 0
MAX_LOAD = 10

MAX_LEN_WIRELESS_NAME = 7

# FUNCTION

def launch_covid19_scrapper():
    def child():
        while True:
            try:
                data = urllib.request.urlopen(COVID19_API_URL).read().decode('utf-8')
                j = json.loads(data)
                with open(COVID19_CACHE_PATH, "w+") as handler:
                    handler.write(str(j['latest']))
            except:
                pass
            time.sleep(60 * 5) # 5 min

    pid = os.fork()
    if pid == 0:
        child()

def get_covid19_data():
    try:
        with open(COVID19_CACHE_PATH, "r") as handler:
            nb = handler.read()
        return "Covid19: " + nb
    except Exception:
        return "Covid19: NO DATA"



def get_wireless_json_part(json):
    for e in json:
        if e and 'name' in e and e['name'] == 'wireless':
            return e
    return None


def minimize_wireless_msg(json):
    try:
        text = json['full_text']

        if "no wlan" in text:
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

    cpujson['color'] = color_get(value, MIN_CPU, MAX_CPU)


def update_load(loadjson):
    text = loadjson['full_text']
    text = text.replace('load ', '')
    text = ''.join(text.split(' '))
    text = text.replace(',', '.')

    loadjson['color'] = color_get(float(text), MIN_LOAD, MAX_LOAD)


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


def normalize_ram(ram):
    if (ram <= 999):
        return str(ram) + "Mib"
    else:
        ram = round(ram/1000, 1)
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
    except Exception as e:
        raise e
        return "ERROR", BLK


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
    launch_covid19_scrapper()

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

        # Covid19
        j.insert(9,
                 {
                     'name': 'Covid19',
                     'markup': 'none',
                     'color': '#F12F2F',
                     'full_text': '%s' % get_covid19_data()
                 })

        # and echo back new encoded json
        print_line(prefix+json.dumps(j))
