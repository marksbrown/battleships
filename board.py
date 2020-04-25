"""
Draw the current board
"""
import pyxel
from random import choice, choices, random, randint, shuffle
from itertools import tee
from config import SHIP_COLOUR, VERBOSE, DEAD_SHIP_COLOUR, TEXT_COLOUR, GRID_COLOUR, SHIP_LENGTHS


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Board:
    """
    Draw N x N board
    Populate board based on clicks
    """
    def __init__(self, N, side, **kwargs):
        assert N > 1, "sanity check"
        self.N = N
        self.side = side
        self.dead_ships = []
        
        # populate ships

        #shuffle(ship_lengths)
        self.ships = []
        self.ship_lengths = kwargs.get('ship_lengths', SHIP_LENGTHS)
        for length in self.ship_lengths:
            self.randomly_place_ship(length) 
        
        assert len(set(self.ships)) == sum(self.ship_lengths), "Incorrect number of ships placed!"

        # coordinates of all ships (game ends when this is empty!)
        self.grid_colour = kwargs.get('grid_colour', GRID_COLOUR)
        #self.missed_colour = kwargs.get('missed_colour', 3)
        #self.hit_colour = kwargs.get('hit_colour', 4)
        self.offset_x = kwargs.get('offset_x', 0)
        self.offset_y = kwargs.get('offset_y', 0)
        self.draw_all_ships = kwargs.get('draw_all_ships', False)  # cheat!


    def randomly_place_ship(self, length, attempts = 5):
        """
        Randomly pick a row or column of data
        pass through the row looking for gaps big enough for length
        if none go back to picking randomly
        Place ship randomly into space(s) available.

        attempts : gives up if this is too low
        """
        while attempts:
            attempts -= 1
            
            axes = randint(0, self.N - 1)
            vertical = choice((-1,1))  # reverse or not reverse!
            to_check = [[axes, j][::vertical] for j in range(self.N)]
            split_on = [index for index, loc in enumerate(to_check) if tuple(loc) in self.ships]
            split_on = [0] + split_on + [self.N - 1]  # minimum of two elements present!
            potentials = []
            for start_index, end_index in pairwise(split_on):
                if end_index - length < start_index + 1:  # ship won't fit!
                    continue
                elif end_index - length == start_index + 1:
                    start_ship = start_index + 1
                else:
                    start_ship = randint(start_index + 1, end_index - length)
                new_ship = [[axes, j][::vertical] for j in range(start_ship, start_ship + length)]
                potentials.append(new_ship)

            if potentials:
                new_ship = [tuple(pair) for pair in choice(potentials)]
                if VERBOSE:
                    print(f"Potential locations for ships : {potentials}")
                    print(f"Placing ship across {new_ship}")
                self.ships += new_ship
                break

    def x(self, index):
        return self.offset_x + index * self.side

    def y(self, index):
        return self.offset_y + index * self.side

    def draw_cell(self, i, j, col, filled=False):
        shape = pyxel.rect if filled else pyxel.rectb
        shape(self.x(i), self.y(j), self.side, self.side, col)
        
    def draw_grid(self):
        for i in range(self.N):
            for j in range(self.N):
                self.draw_cell(i, j, self.grid_colour)

    def draw_ships(self):
        if self.draw_all_ships:
            for loc in self.ships:
                self.draw_cell(*loc, SHIP_COLOUR, filled=True)
        for loc in self.dead_ships:
            self.draw_cell(*loc, DEAD_SHIP_COLOUR, filled=True)

    def score(self):
        return len(self.dead_ships)*10

    def draw(self):
        self.draw_grid()
        pyxel.text(self.offset_x, 10, f"Score {self.score():03}", TEXT_COLOUR)
        pyxel.text(self.offset_x, 20, f"Alive : {len(self.ships)} Dead : {len(self.dead_ships)}", TEXT_COLOUR)