import pyxel
from random import shuffle

class Enemy:
    """
    Aim to destroy all ships present!
    """

    def __init__(self, board, **kwargs):
        self.board = board
        self.colour = kwargs.get('colour', 5)

    def next_move(self):
        """
        returns next move after all locations created and then shuffled
        priority tiles (ie next to a win) are put to the front of the queue!
        """

        self.potential_moves = [[[i,j] for i in range(self.board.N)] for j in range(self.board(N))]
        shuffle(self.potential_moves)

        yield self.potential_moves.pop(0)


