import pygame as pg

from game_objects.game_object import CollidedObject, CollidingObject
from util import *


class Target(CollidedObject):
    """
    Target class. Creates target, manages it's rendering and collision with a ball event.
    """

    def __init__(self, coord=None, color=None, size=30):
        self.shot = False
        if coord is None:
            coord = random_coord(size)
        super().__init__(coord, False, 0, size, color)

    def update(self, events=None, time=1, game_manager=None):
        pass

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.size)

    def destroy_ready(self) -> bool:
        return self.shot

    def proceed_collide(self, colliding_object):
        if colliding_object.is_ally() and do_touch(self, colliding_object):
            self.shot = True

