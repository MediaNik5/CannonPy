from game_objects.game_object import GameObject, SCREEN_SIZE
from game_objects.shell import Shell
from game_objects.game_object import pg
import numpy as np

from constants import RED, velocity_scale


class Gun(GameObject):

    def __init__(self, initial_size=5, coord=None, angle=0, max_pow=30, min_pow=1, color=RED):
        if coord is None:
            coord = [30, SCREEN_SIZE[1] // 2]
        super().__init__(coord, True, (0, 0), initial_size, color)

        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow
        self.active = False
        self.pow = min_pow

    def update(self, events=None, time=1, game_manager=None):
        self.gain_pow(time)
        self.direct_to_mouse()
        self.handle_events(events, game_manager)

    def gain_pow(self, time):
        if self.active and self.pow < self.max_pow:
            self.pow += 2 * time

    def direct_to_mouse(self):
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.set_angle(mouse_pos)

    def set_angle(self, target_pos):
        x = target_pos[0] - self.coord[0]
        y = target_pos[1] - self.coord[1]
        self.angle = np.arctan2(y, x)

    def handle_events(self, events, game_manager):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == (pg.K_UP or pg.K_w):
                    self.move(0, -5)
                elif event.key == (pg.K_DOWN or pg.K_s):
                    self.move(0, 5)
                elif event.key == (pg.K_LEFT or pg.K_a):
                    self.move(-5, 0)
                elif event.key == (pg.K_RIGHT or pg.K_d):
                    self.move(5, 0)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.active = False
                    shell = self.strike()
                    game_manager.game_objects.add(shell)

    def strike(self) -> Shell:

        velocity = self.pow
        velocity = [velocity * np.cos(self.angle)*velocity_scale, velocity * np.sin(self.angle)*velocity_scale]

        shell = Shell(list(self.coord), velocity)

        self.pow = self.min_pow
        self.active = False
        return shell

    def destroy_ready(self) -> bool:
        return False

    def draw(self, screen):

        far_left_point, far_right_point, near_left_point, near_right_point = self.calculate_points()

        gun_shape = [near_left_point,
                     far_left_point,
                     far_right_point,
                     near_right_point]

        pg.draw.polygon(screen, self.color, gun_shape)

    def calculate_points(self):
        parallel_vector, perpendicular_vector = self.calculate_sizes()

        gun_pos = np.array(self.coord)
        near_left_point = (gun_pos + perpendicular_vector).tolist()
        far_left_point = (gun_pos + perpendicular_vector + parallel_vector).tolist()
        near_right_point = (gun_pos - perpendicular_vector).tolist()
        far_right_point = (gun_pos + parallel_vector - perpendicular_vector).tolist()

        return far_left_point, far_right_point, near_left_point, near_right_point

    def calculate_sizes(self) -> ([int, int], [int, int]):
        perpendicular_angle = self.angle - np.pi / 2
        perpendicular_vector = np.array([self.size * np.cos(perpendicular_angle),
                                         self.size * np.sin(perpendicular_angle)])
        parallel_vector = np.array([self.pow * np.cos(self.angle),
                                    self.pow * np.sin(self.angle)])
        return parallel_vector, perpendicular_vector
