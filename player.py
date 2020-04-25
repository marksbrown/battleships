import pyxel
from config import SHOT_COLOUR, VERBOSE
from abc import abstractmethod, ABC


class Player(ABC):

    @property
    def size(self):
        return self.board.side
    
    def __init__(self, board, colour, **kwargs):
        self.board = board  # which board is this player playing on!
        self.colour = colour

        # Initial position
        self.i, self.j = [self.board.N // 2,]*2
        self.shots_fired = kwargs.get('shots_fired', [])

        # Weapons details
        self.shot_radius = 0  # 0 is not fired
        self.shot_colour = kwargs.get('shot_colour', SHOT_COLOUR)
        
        assert isinstance(self.shots_fired, list), "Have you changed how shots are tracked?"
        assert 0 <= self.i < self.board.N, "invalid initial position (x)"
        assert 0 <= self.j < self.board.N, "invalid initial position (y)"

    @abstractmethod
    def update(self):
        pass

    def fire_shot(self, x, y):
        """
        Returns True if shot lands on ship
        """
        self.shots_fired.append((x,y))
        self.shot_radius = self.size + self.size // 10
        
        if (x,y) in self.board.ships:
            if VERBOSE:
                print(f"A Hit! at : {x},{y}")
            self.board.ships.remove((x,y))
            self.board.dead_ships.append((x,y))
            return True
        return False

    def draw(self):
        x = self.board.x(self.i)
        y = self.board.y(self.j)
        pyxel.rect(x, y, self.size, self.size, self.colour)

        if self.shot_radius:
            delta = self.size // 2  # offset to centre!
            pyxel.circ(x+delta,y+delta,self.shot_radius, self.shot_colour)
            self.shot_radius -= 1

        for loc in self.shots_fired:
            self.board.draw_cell(*loc, self.shot_colour, filled=True)

        self.board.draw_ships()