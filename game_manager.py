from game_objects.gun import Gun
from game_objects.game_object import CollidedObject, CollidingObject, pg, GameObject
from game_objects.target import Target


class GameManager:
    """
    Class that manages game events, shell
    """

    def __init__(self, number_of_targets=0):
        self.game_objects = {Target((0, 0), False)}
        self.game_objects.clear()

        self.collided_pairs = {}
        self.number_of_targets = number_of_targets

        self.new_mission()

    def new_mission(self):
        """
        Adds new targets
        :return:
        """
        for i in range(self.number_of_targets):
            target = Target()
            self.game_objects.add(target)
        self.game_objects.add(Gun())

    def process(self, events, screen) -> bool:
        """
        Runs all methods for each iteration. Adds new targets if needed.
        :return: True if it will exit app, False otherwise.
        """
        self.move_all(events)
        self.collide_all()
        self.draw_all(screen)

        return self.handle_events(events)

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pg.QUIT:
                return True
        return False

    def move_all(self, events):
        """
        Moves all movable things that need to be moved.
        """
        temp_game_objects = self.game_objects.copy()
        for game_object in temp_game_objects:
            game_object.update(events, game_manager=self)
            if game_object.destroy_ready():
                game_object.destroy()
                self.game_objects.remove(game_object)

    def collide_all(self):
        """
        Collides all things that need to be collided.
        """
        temp_game_objects = self.game_objects.copy()
        for target in temp_game_objects:
            if not isinstance(target, CollidedObject):
                continue

            for hitter in temp_game_objects:
                if not isinstance(hitter, CollidingObject):
                    continue
                if target is hitter:
                    continue

                if (hitter, target) in self.collided_pairs.keys() or (target, hitter) in self.collided_pairs.keys():
                    self.collided_pairs[hitter, target] -= 1
                    self.collided_pairs[target, hitter] -= 1
                    if self.collided_pairs[hitter, target] < 0 or self.collided_pairs[target, hitter] < 0:
                        self.collided_pairs.pop((hitter, target))
                        self.collided_pairs.pop((target, hitter))
                    else:
                        continue

                target.proceed_collide(hitter)
                self.collided_pairs[hitter, target] = 20
                self.collided_pairs[target, hitter] = 20
                if target.destroy_ready():
                    target.destroy()
                    if target in self.game_objects:  # might be that target is already out of game_objects, but for cycle goes
                        if isinstance(target, Target):
                            self.game_objects.remove(target)
                            self.game_objects.add(Target())
                        else:
                            self.game_objects.remove(target)

    def draw_all(self, screen):
        for obj in self.game_objects:
            obj.draw(screen)
