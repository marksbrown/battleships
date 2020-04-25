import pyxel
from random import shuffle
from battleships.config import ENEMY_COLOUR, VERBOSE, FPS
from battleships.player import Player

class Enemy(Player):
    """
    Enemy class

    Holds everything to do with the Enemy
    """
    def __init__(self, board, **kwargs):
        colour = kwargs.get('colour', ENEMY_COLOUR)
        super().__init__(board, colour, **kwargs)
    
        ## How often the computer guesses!
        self.countdown = 0
        self.cooldown = kwargs.get('cooldown', 2)

        self._generate_all_moves()

    def _generate_all_moves(self):
        self.potential_moves = []
        for i in range(self.board.N):
            for j in range(self.board.N):
                self.potential_moves.append([i,j])
        
        shuffle(self.potential_moves)

    def next_move(self):
        """
        returns next move after all locations created and then shuffled
        priority tiles (ie next to a win) are put to the front of the queue!
        """
        return self.potential_moves.pop(0)
            
    def prioritise_adjacent(self, x, y):
        """
        Move shots adjacent to successful shot to front of queue
        """
        to_shift = []
        L = 1
        for index, (new_x, new_y) in enumerate(self.potential_moves):
            if new_x in range(x-L, x+2*L, L) and new_y in range(y-L, y+2*L, L):
                to_shift.append(index)

        # Places all adjacent tiles at the front of the queue
        for index in to_shift:
            self.potential_moves.insert(0, self.potential_moves.pop(index))

    def update(self):
        if not self.countdown:
            self.countdown += self.cooldown
            self.i, self.j = self.next_move()
            if self.fire_shot(self.i, self.j):
                self.prioritise_adjacent(self.i, self.j)

        else:
            self.countdown -= 1


