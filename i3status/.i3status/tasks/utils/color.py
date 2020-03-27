import pickle

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
    color_id = int((val - mini) / step)
    return COLOR[color_id if color_id < NBCOLOR else -1]

color_init()
