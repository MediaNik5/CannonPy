from game_objects.game_object import pg
from game_manager import GameManager
from game_objects.shell import Shell
from constants import BLACK, SCREEN_SIZE

go = Shell(0, 0)
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("The cannon game")

done = False
clock = pg.time.Clock()

mg = GameManager()

while not done:
    clock.tick(200)
    screen.fill(BLACK)

    done = mg.process(pg.event.get(), screen)

    pg.display.flip()

pg.quit()

