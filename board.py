"""
Draw the current board
"""
import pyxel
from random import choice, choices, random, randint, shuffle
from itertools import tee
from config import SHIP_COLOUR, VERBOSE, DEAD_SHIP_COLOUR, TEXT_COLOUR

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
    def __init__(self, N, side, ship_lengths, **kwargs):
        assert N > 1, "sanity check"
        self.N = N
        self.side = side
        self.dead_ships = []
        self.ships = kwargs.get('ship_locations', [])  # override for Player
        if not self.ships:
            shuffle(ship_lengths)
            for length in ship_lengths:
                self.ships += self.randomly_place_ship(length)
        if VERBOSE:
            print(f"{len(self.ships)} Ships assigned to", self.ships)

        assert len(self.ships) == sum(ship_lengths), "Incorrect number of ships placed!"

        # coordinates of all ships (game ends when this is empty!)
        self.grid_colour = kwargs.get('grid_colour', 2)
        self.missed_colour = kwargs.get('missed_colour', 3)
        self.hit_colour = kwargs.get('hit_colour', 4)
        self.offset_x = kwargs.get('offset_x', 0)
        self.offset_y = kwargs.get('offset_y', 0)
        self.draw_ships = kwargs.get('draw_ships', False)  # cheat!


    def randomly_place_ship(self, length):
        """
        Randomly pick a row or column of data
        pass through the row looking for gaps big enough for length
        if none go back to picking randomly
        Place ship randomly into space(s) available.
        """
        while True:
            axes = randint(0, self.N - 1)
            vertical = choice((-1,1))  # reverse or not reverse!
            to_check = [[axes, j][::vertical] for j in range(self.N)]
            split_on = [index for index, loc in enumerate(to_check) if loc in self.ships]
            split_on = [0] + split_on + [self.N - 1]  # minimum of two elements present!
            potentials = []
            for start_index, end_index in pairwise(split_on):
                if end_index - start_index < length:
                    continue
                start_ship = randint(start_index, end_index - length)
                new_ship = [[axes, j][::vertical] for j in range(start_ship, start_ship + length)]
                potentials.append(new_ship)

            if potentials:
                return choice(potentials)

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

    def draw(self):
        self.draw_grid()
        if self.draw_ships:
            for loc in self.ships:
                self.draw_cell(*loc, SHIP_COLOUR, filled=True)
        for loc in self.dead_ships:
            self.draw_cell(*loc, DEAD_SHIP_COLOUR, filled=True)

        pyxel.text(self.offset_x, 10, f"Score {len(self.dead_ships)*10:03}", TEXT_COLOUR)