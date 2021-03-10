from abc import ABC, abstractmethod

import pygame as pg

pg.init()
pg.font.init()


class GameObject(ABC):

    def __init__(self, coord, ally: bool, velocity=(0, 0), size=0, color=None):
        self.coord = coord
        self.velocity = velocity
        self.is_alive = True
        self.ally = ally

        self.size = size
        if color is None:
            self.color = random_color()
        else:
            self.color = color

    @abstractmethod
    def update(self, events=None, time=1, game_manager=None):
        """
        Moves the object according it's speed and time.
        Changes the object's velocity due to gravitation acceleration if needed.
        :param game_manager:
        :param events: Events of pygame
        :param time: The time multiplier. More == faster, takes "less real time" to update.
        """
        pass

    @abstractmethod
    def draw(self, screen):
        """
        Draws the object on the screen
        """
        pass

    @abstractmethod
    def destroy_ready(self) -> bool:
        """
        Indicates whether the object should be destroyed or not.
        :return: True if the object should be destroyed, False otherwise.
        """
        pass

    def is_ally(self) -> bool:
        return self.ally

    def is_enemy(self) -> bool:
        return not self.ally

    def destroy(self):
        self.move = lambda: None
        self.draw = lambda: None
        self.is_alive = False

    def is_alive(self):
        return self.is_alive


from util import *


class CollidedObject(GameObject):
    """
    Class of Object that might be collied by a CollidingObject instance.
    """

    def __init__(self, coord, ally: bool, velocity=0, size=20, color=None):
        GameObject.__init__(self, coord, ally, velocity, size, color)

    @abstractmethod
    def proceed_collide(self, colliding_object):
        pass


class CollidingObject(GameObject):
    """
    Class of Object that might init_collide a CollidedObject instance.
    """

    def __init__(self, coord, ally: bool, velocity=0, size=20, color=None):
        super().__init__(coord, ally, velocity, size, color)

    @abstractmethod
    def init_collide(self, collided_object: CollidedObject):
        """
        The process of colliding the object.
        """
        pass
