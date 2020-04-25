"""
Battleships Implementation using Pyxel
"""

import pyxel
from config import SCREEN_SIZE, DEFAULT_CAPTION, TEXT_COLOUR, FPS, BACKGROUND_COLOUR, VERBOSE
from board import Board
from human import Human
from enemy import Enemy

from time import sleep

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
                           draw_all_ships = False,
                           offset_x = 10, 
                           offset_y = 30)
        self.right_board = Board(self.max_index, self.grid_size, 
                           draw_all_ships = False,
                           offset_x = 30 + self.grid_size * self.max_index, 
                           offset_y = 30)

        if VERBOSE:
            self.number_of_players = 0
        else:
            self.number_of_players = self.welcome_screen()

        for i in range(5,0,-1):
            print(i)
            sleep(1)

        if self.number_of_players == 2:
            self.left_player = Human(self.left_board, arrow_keymap)
            self.right_player = Human(self.right_board, wasd_keymap)
        elif self.number_of_players == 1:
            self.left_player = Human(self.left_board, arrow_keymap)
            self.right_player = Enemy(self.right_board)
        else:
            self.left_player = Enemy(self.left_board)
            self.right_player = Enemy(self.right_board)

        pyxel.init(*SCREEN_SIZE, caption=DEFAULT_CAPTION, 
                    fps=FPS, quit_key=pyxel.KEY_Q)
        pyxel.run(self.update, self.draw)

    @staticmethod
    def welcome_screen(linewidth=80, fillchar='='):
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


    def game_over(self):
        winner = 'left' if not self.left_board.ships else 'right'
        sx, sy = SCREEN_SIZE
        sx //= 3
        sy = self.grid_size*self.max_index + 32
        blurb = ['Game Over!',
                f'Player {winner} wins!',
                f'Player One Score : {self.left_board.score():03}',
                f'Player Two Score : {self.right_board.score():03}']
        blurb = "\n".join(blurb)
        
        pyxel.text(sx, sy, blurb, TEXT_COLOUR)
        
    def update(self):
        if self.end_game:
            return
        self.left_player.update()
        self.right_player.update()

        if not self.left_board.ships or not self.right_board.ships:
            self.end_game = True

    def draw(self):
        pyxel.cls(BACKGROUND_COLOUR)
        if self.end_game:
            self.game_over()
        
        self.left_board.draw()
        self.right_board.draw()

        self.left_player.draw()
        self.right_player.draw()
        
        

if __name__ == "__main__":
    Game()