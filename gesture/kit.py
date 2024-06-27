import numpy as np
import pyautogui as pg

pg.PAUSE = 0
pg.MINIMUM_DURATION = 0
pg.MINIMUM_SLEEP = 0

def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def LineMag(points: list):
    total_distance = 0.0
    for i in range(len(points) - 1):
        total_distance += distance(points[i], points[i + 1])
    return total_distance

def R_Sq(points):
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]

    slope, intercept = np.polyfit(x, y, 1)

    y_pred = slope * x + intercept
    r_squared = 1 - (np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2))

    return r_squared

def slow_scroll(px):
    if px > 0:
        for i in range(int(px / 10)):
            pg.scroll(10)
            pg.sleep(0.004)
    else:
        for i in range(int(px / 10) * -1):
            pg.scroll(-10)
            pg.sleep(0.004)

def get_swipe_direction(path):
    if len(path) < 2:
        return None
    
    start_x, start_y = path[0]
    end_x, end_y = path[-1]

    delta_x = end_x - start_x
    delta_y = end_y - start_y

    min_distance_threshold = 50

    if abs(delta_x) > abs(delta_y):
        if abs(delta_x) > min_distance_threshold:
            if delta_x > 0:
                pg.hotkey("ctrl", "win", "right")
                pg.sleep(2)
                return "Right"
            else:
                pg.hotkey("ctrl", "win", "left")
                pg.sleep(2)
                return "Left"
    else:
        if abs(delta_y) > min_distance_threshold:
            if delta_y > 0:
                slow_scroll(-700)
                return "Bottom"
            else:
                slow_scroll(700)
                return "Top"
    return None
