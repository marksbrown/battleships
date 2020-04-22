import pyxel
from config import PLAYER_COLOUR, SHOT_COLOUR, VERBOSE

class Player:
    """
    Player class

    Holds everything to do with the player including previous shots
    """
    def __init__(self, board, keymap, **kwargs):
        self.colour = kwargs.get('player_colour', PLAYER_COLOUR)
        self.board = board  # which board is this player playing on!
        self.keymap = keymap

        # Initial position
        self.i = kwargs.get('index_x', 0)
        self.j = kwargs.get('index_y', 0)
        self.shots_fired = kwargs.get('shots_fired', [])
        self.size = kwargs.get('size', 10)

        # Weapons details
        self.shot_radius = 0
        self.shot_colour = kwargs.get('shot_colour', SHOT_COLOUR)
        
        assert isinstance(self.shots_fired, list), "Have you changed how shots are tracked?"

        assert 0 <= self.i < self.board.N, "invalid initial position (x)"
        assert 0 <= self.j < self.board.N, "invalid initial position (y)"

    def update(self):
        for key in self.keymap:
            if pyxel.btnp(key):
                x,y = self.keymap[key]
                if 0 <= self.i+x < self.board.N:
                    self.i += x
                if 0 <= self.j+y < self.board.N:
                    self.j += y

                if not x and not y:  # weapon's fire!
                    if (self.i, self.j) not in self.shots_fired:  # can't fire at the same place twice!
                        self.fire_shot(self.i,self.j)

    def fire_shot(self, x, y):
        if VERBOSE:
            print(f"Shot fired at {x},{y}")

        self.shots_fired.append((x,y))
        self.shot_radius = self.size + 2

    def draw(self):
        x = self.board.x(self.i)
        y = self.board.y(self.j)
        pyxel.rect(x,y, self.size, self.size, self.colour)

        if self.shot_radius:
            delta = self.size // 2  # offset to centre!
            pyxel.circ(x+delta,y+delta,self.shot_radius, self.shot_colour)
            self.shot_radius -= 1

        for loc in self.shots_fired:
            self.board.draw_cell(*loc, self.shot_colour, filled=True)
