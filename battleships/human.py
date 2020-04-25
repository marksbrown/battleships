import pyxel
from battleships.config import HUMAN_COLOUR, VERBOSE
from battleships.player import Player

class Human(Player):
    """
    Human class

    Holds everything to do with the player
    """
    def __init__(self, board, keymap, **kwargs):
        colour = kwargs.get('colour', HUMAN_COLOUR)
        self.keymap = keymap
        super().__init__(board, colour, **kwargs)
        
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
                        if self.fire_shot(self.i,self.j):
                            pass  # Place for further animation function call

