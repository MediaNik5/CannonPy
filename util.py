from random import randint
import numpy as np

from game_objects.game_object import GameObject
from constants import SCREEN_SIZE


def random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def random_coord(size: int):
    return [randint(size, SCREEN_SIZE[0] - size), randint(size, SCREEN_SIZE[1] - size)]


def distance(obj1: GameObject, obj2: GameObject) -> int:
    return np.sqrt((obj1.coord[0] - obj2.coord[0]) ** 2 + (obj1.coord[1] - obj2.coord[1]) ** 2)


def proj(b: [float, float], a: [float, float]) -> [float, float]:
    length_squared = a[0] ** 2 + a[1] ** 2
    if length_squared == 0:
        multiplier = 0
    else:
        multiplier = (a[0]*b[0] + a[1]*b[1])/(length_squared)
    return [a[0]*multiplier, a[1]*multiplier]


def vector(start: [float, float], end: [float, float]) -> [float, float]:
    return [end[0] - start[0], end[1] - end[0]]


def do_touch(object1: GameObject, object2: GameObject) -> bool:
    if distance(object1, object2) <= object2.size + object1.size:
        return True
    return False


def module(vector: [float, float]) -> float:
    return np.sqrt(vector[0] ** 2 + vector[1] ** 2)


def collide_velocities(v1: [float, float], v2: [float, float]) -> ([float, float], [float, float]):
    theta1 = np.arctan2(v1[0], v1[1])
    theta2 = np.arctan2(v2[0], v2[1])
    phi = abs(theta2 - theta1)
    v1_module = module(v1)
    v2_module = module(v2)
    v1x = v2_module*np.cos(theta2 - phi)*np.cos(phi) - v1_module*np.sin(phi)*np.sin(theta1 - phi)
    v2x = v1_module*np.cos(theta1 - phi)*np.cos(phi) - v2_module*np.sin(phi)*np.sin(theta2 - phi)

    v1y = v2_module*np.cos(theta2 - phi)*np.sin(phi) - v1_module*np.cos(phi)*np.sin(theta1 - phi)
    v2y = v1_module*np.cos(theta1 - phi)*np.sin(phi) - v2_module*np.cos(phi)*np.sin(theta2 - phi)

    return [v1x, v1y], [v2x, v2y]
