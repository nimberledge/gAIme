import pygame
from boardslot import *

class TicTacToeBoard(object):

    def __init__(self, screen, game_state=None):
        """
        Constructor for the board object. Should initialize a variable called self.grid to store state.
        State is represented by a single list [a0, a1, a2..a8].
        They correspond to positions on the board as follows:

        a0 a1 a2
        a3 a4 a5
        a6 a7 a8

        game_state is an argument for the game state passed. It will be in the type described above for a state.
        If game_state is not None, initialize the board to the state in game_state.
        """
        self.grid = []
        if game_state is not None:
            self.state = game_state
        else:
            self.state = [None for i in range(9)]
        self.initialize_grid(screen)
        self.player_turn = 0

    def initialize_grid(self, screen):
        screen_size = screen.get_size()
        side = 0
        if screen_size[0] < screen_size[1]:
            side = int(screen_size[0] / 5)
        else:
            side = int(screen_size[1] / 5)
        center_x = int(screen_size[0] / 2)
        center_y = int(screen_size[1] / 2)
        center_x -= (side / 2)
        center_y -= (side / 2)

        row = 0
        for i in range(9):
            position = []
            if i == 0 or i == 3 or i == 6:
                x = center_x - side
                y = center_y
                if row == 0:
                    y = y - side
                elif row == 2:
                    y = y + side
                position.append(x)
                position.append(y)
            elif i == 2 or i == 5 or i == 8:
                x = center_x + side
                y = center_y
                if row == 0:
                    y = y - side
                elif row == 2:
                    y = y + side
                position.append(x)
                position.append(y)
            else:
                x = center_x
                y = center_y
                if row == 0:
                    y = y - side
                elif row == 2:
                    y = y + side
                position.append(x)
                position.append(y)
            ob = BoardSlot(side, position, i)
            self.grid.append(ob)
            if i == 2 or i == 5:
                row += 1

    def draw(self, screen):
        for slot in self.grid:
            slot.draw(screen)

    def update_board(self, mpos):
        """
        Updates board-object's state based on mouseclick position - mpos.
        """
        self.player_turn = sum([1 for el in self.state if el])
        if self.player_turn >= 9: #If endgame, don't register the click
            return None
        for slot in self.grid:
            #If a slot is clicked and it has not been clicked before, update the symbol of that slot
            if slot.is_clicked(mpos) and slot.get_symbol() == None:
                ind = self.grid.index(slot)
                symbol = ('X', 'O')[self.player_turn % 2]
                self.state[ind] = symbol
                #Determine which player's turn it is
                if self.player_turn % 2 == 1:
                    slot.update(symbol)
                elif self.player_turn % 2 == 0:
                    slot.update(symbol)
                return True
        return False

    def update_to_state(self, game_state):
        """
        Updates the board-object's state to the game_state passed where game state is of the type described
        in the constructor.
        """
        self.player_turn = sum([1 for el in self.state if el])
        self.state = list(game_state)
        for i, slot in enumerate(self.grid):
            if slot.val != self.state[i]:
                slot.val = self.state[i]
                break

#########################################
'''
Test play method
'''

def play():
    pygame.init()
    screen = pygame.display.set_mode((500, 800))
    background = pygame.Surface((500, 800))
    background.fill((255, 255, 255))
    board = TicTacToeBoard(screen)
    board.draw(screen)
    pygame.display.update()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                board.update_board(mpos)
                board.draw(screen)
                pygame.display.update()
            if board.player_turn > 9:
                done = True
                break
    quit()

if __name__ == '__main__':
    play()
