"""
Battleships Implementation using Pyxel
"""

import pyxel
from config import SCREEN_SIZE, DEFAULT_CAPTION, TEXT_COLOUR, FPS
from board import Board
from player import Player
from enemy import Enemy

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
        self.end_game = False
        self.left_board = Board(self.max_index, self.grid_size, 
                           ship_lengths = [2,3,4,5], draw_ships = True,
                           offset_x = 10, offset_y = 30)
        self.right_board = Board(self.max_index, self.grid_size, 
                           ship_lengths = [2,3,4,5], draw_ships = True,
                           offset_x = 30 + self.grid_size * self.max_index, offset_y = 30)

        self.number_of_players = self.welcome_screen()

        left_kwargs = dict(board=self.left_board, keymap=arrow_keymap)
        right_kwargs = dict(board=self.right_board, keymap=wasd_keymap)
        if self.number_of_players == 2:
            self.players = [Player(**left_kwargs), Player(**right_kwargs)]
        elif self.number_of_players == 1:
            self.players = [Player(**left_kwargs), Enemy(**right_kwargs)]
        else:
            self.players = [Enemy(**left_kwargs), Enemy(**right_kwargs)]

        pyxel.init(*SCREEN_SIZE, caption=DEFAULT_CAPTION, 
                    fps=FPS, quit_key=pyxel.KEY_Q)
        pyxel.run(self.update, self.draw)

    def welcome_screen(self, linewidth=80, fillchar='='):
        print("Battleships!".center(linewidth, fillchar))
        print("\n\n")
        pre = "! Human Error Detected !\n"
        while True:
            try:
                humans = int(input("How many HUMAN players (0, 1, 2)?"))
            except ValueError:
                print(pre+"Integer number of humans only")
                continue

            if 0 <= humans <= 2:
                return humans
            elif humans < 0:
                print(pre+"Real quantities of humans only")
            elif humans > 2:
                print(pre+"Excess of humans, cannot comply")

    def update(self):
        for player in self.players:
            player.update()

        if not self.left_board.ships or not self.right_board.ships:
            self.end_game = True

    def game_over(self):
        winner = 'left' if not self.left_board.ships else 'right'
        sx, sy = SCREEN_SIZE
        sx //= 3
        sy //= 2
        pyxel.text(sx, sy, f"{winner} player wins!", TEXT_COLOUR)
            
      
    def draw(self):
        pyxel.cls(0)
        if self.end_game:
            self.game_over()
        else:
            self.left_board.draw()
            self.right_board.draw()

            for player in self.players:
                player.draw()

            
        

if __name__ == "__main__":
    Game()