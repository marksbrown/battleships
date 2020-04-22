"""
Battleships Implementation using Pyxel
"""

import pyxel
from config import SCREEN_SIZE, DEFAULT_CAPTION
from board import Board
from player import Player

arrow_keymap = {pyxel.KEY_UP : (0, -1),
                pyxel.KEY_DOWN : (0, 1),
                pyxel.KEY_LEFT : (-1, 0),
                pyxel.KEY_RIGHT : (1, 0),
                pyxel.KEY_SPACE : (0, 0)}
    
wasd_keymap = {pyxel.KEY_W : (0, -1),
            pyxel.KEY_S : (0, 1),
            pyxel.KEY_A : (-1, 0),
            pyxel.KEY_D : (1, 0),
            pyxel.KEY_E : (0, 0)}


class Game:
    def __init__(self, **kwargs):
        self.grid_size = kwargs.get('grid_size', 10)
        self.max_index = kwargs.get('N', 10)
        
        self.left_board = Board(self.max_index, self.grid_size, 
                           ship_lengths = [2,3,4,5], draw_ships = True,
                           offset_x = 10, offset_y = 30)
        self.right_board = Board(self.max_index, self.grid_size, 
                           ship_lengths = [2,3,4,5], draw_ships = True,
                           offset_x = 30 + self.grid_size * self.max_index, offset_y = 30)

        self.left_player = Player(player_colour=2, board=self.left_board, keymap=arrow_keymap)
        self.right_player = Player(player_colour=2, board=self.right_board, keymap=wasd_keymap)

        pyxel.init(*SCREEN_SIZE, caption=DEFAULT_CAPTION, quit_key=pyxel.KEY_Q)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.left_player.update()
        self.right_player.update()

    def draw(self):
        pyxel.cls(0)
        self.left_board.draw()
        self.right_board.draw()
        self.left_player.draw()
        self.right_player.draw()


if __name__ == "__main__":
    Game()