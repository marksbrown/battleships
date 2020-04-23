import pyxel
from random import shuffle
from config import ENEMY_COLOUR, SHOT_COLOUR

class Enemy:
    """
    Aim to destroy all ships present!
    """

    def __init__(self, board, **kwargs):
        self.board = board
        self.colour = kwargs.get('colour', ENEMY_COLOUR)
        self.shot_colour = kwargs.get('shot_colour', SHOT_COLOUR)
        self.shot_radius = 0
        self.countdown = 0
        self.cooldown = kwargs.get('cooldown', 48)
        self.i = 0
        self.j = 0
        self.shots_fired = kwargs.get('shots_fired', [])
        self.size = kwargs.get('size', 10)

    def next_move(self):
        """
        returns next move after all locations created and then shuffled
        priority tiles (ie next to a win) are put to the front of the queue!
        """

        self.potential_moves = []
        for i in range(self.board.N):
            for j in range(self.board.N):
                self.potential_moves.append([i,j])
        
        shuffle(self.potential_moves)

        return self.potential_moves.pop(0)

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

    def fire_shot(self):
        self.shot_radius = self.size + 2
        shot_fired = self.next_move()
        self.shots_fired.append(shot_fired)
        self.countdown += self.cooldown
        
        self.i, self.j = shot_fired

        if shot_fired in self.board.ships:
            self.board.ships.remove(shot_fired)
            self.board.dead_ships.append(shot_fired)
            

    def update(self):
        if not self.countdown:
            self.fire_shot()
        else:
            self.countdown -= 1


