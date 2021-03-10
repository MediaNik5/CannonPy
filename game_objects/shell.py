import pygame as pg

from game_objects.game_object import CollidingObject, SCREEN_SIZE, CollidedObject
from constants import gravitation_acceleration
from util import vector, proj, do_touch, collide_velocities


class Shell(CollidingObject, CollidedObject):
    """
    The shell class. Implements its movement and rendering.
    """

    def __init__(self, coord, velocity, size=20, color=None):
        super().__init__(coord, True, velocity, size, color)
        self.collided = None

    def update(self, events=None, time=1, game_manager=None):
        """
        Moves the shell according it's speed and time.
        Changes the shell's velocity due to gravitation acceleration.
        :param game_manager:
        :param events: Not to pass
        :param time: The time multiplier. More == faster, takes "less real time" to update.
        """

        self.velocity[1] += gravitation_acceleration
        for i in range(2):  # both x and y coord
            self.coord[i] += time * self.velocity[i]
        self.handle_borders()

    def destroy_ready(self) -> bool:
        """
        Indicates whether the object should be destroyed or not.
        :return: True if the object should be destroyed, False otherwise.
        """
        return self.velocity_square() < 4 and self.is_lying_on_floor()

    def velocity_square(self) -> int:
        return self.velocity[0] ** 2 + self.velocity[1] ** 2

    def is_lying_on_floor(self) -> bool:
        return self.coord[1] > SCREEN_SIZE[1] - 2 * self.size

    def handle_borders(self, reflection_ort_coeff=0.93, reflection_projection_coeff=0.97):
        """
        Handles rebounce from borders.
        :param reflection_ort_coeff: Coefficient of remaining speed to ort axis:
        e.g. you hit the floor with speed 10 by y, then remaining speed by y to reversed side is
         -10*reflection_ort_coeff
        :param reflection_projection_coeff: Analogue to ort coeff,
        but in that example it would be speed by x
        :return:
        """
        for i in range(2):  # both x and y coord
            if self.coord[i] < self.size:
                self.coord[i] = self.size
                self.__reflect(i, reflection_ort_coeff, reflection_projection_coeff)
            elif self.coord[i] > SCREEN_SIZE[i] - self.size:
                self.coord[i] = SCREEN_SIZE[i] - self.size
                self.__reflect(i, reflection_ort_coeff, reflection_projection_coeff)

    def __reflect(self, axis: int, reflection_ort_coeff: float, reflection_projection_coeff: float):
        """
        :param axis: x if 0, y if 1
        """
        self.velocity[axis] = -self.velocity[axis] * reflection_ort_coeff
        self.velocity[1 - axis] = self.velocity[1 - axis] * reflection_projection_coeff

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.size)

    def init_collide(self, collided_object: CollidedObject):
        self.proceed_collide(collided_object)

    def proceed_collide(self, collided_object: CollidedObject):
        if not isinstance(collided_object, Shell):
            return
        if self is collided_object:
            return
        if self.collided is collided_object:
            self.collided = None
            return
        if not do_touch(self, collided_object):
            return

        self.velocity, collided_object.velocity = collide_velocities(self.velocity, collided_object.velocity)

        collided_object.collided = self


















