from orderandchaosstate import OrderAndChaosState
import pygame
import random
import time
pygame.font.init()

class GridSquare(object):
    border_colour = (255, 255, 255)
    text_colour = (255, 255, 255)
    highlight_colour = (0, 0, 255)
    font = pygame.font.SysFont('Times New Roman', 35)

    def __init__(self, x, y, value = None, side_length=25, highlighted=False):
        self.side_length = side_length
        self.screen_pos = (x, y)
        if value:
            self.value = value
        else:
            self.value = ''
        self.highlighted = highlighted
        self.rect = pygame.Rect(x, y, self.side_length, self.side_length)

    def draw(self, screen):
        pygame.draw.rect(screen, self.border_colour, self.rect, 1)
        if self.value:
            if self.highlighted:
                text = self.font.render(self.value, True, self.highlight_colour)
            else:
                text = self.font.render(self.value, True, self.text_colour)

            screen.blit(text,
                        (self.screen_pos[0] + self.side_length / 2 - text.get_width() / 2,
                         self.screen_pos[1] + self.side_length / 2 - text.get_height() / 2))

    def is_clicked(self, mpos):
        if self.screen_pos[0] <= mpos[0] <= self.screen_pos[0] + self.side_length and self.screen_pos[1] <= mpos[1] <= \
                        self.screen_pos[1] + self.side_length:
            return True
        return False

    def update_value(self, value):
        self.value = value


class OrderAndChaosBoard(object):

    def __init__(self, screen, dict_representation=None):
        self.grid = []
        self.symbol_boxes = []
        self.__get_grid(screen)
        if dict_representation:
            self.grid_from_dict(dict_representation)
        else:
            self.dict_representation = dict(zip([(i,j) for i in range(6) for j in range(6)], [None for i in range(36)]))

    def __get_grid(self, screen):
        screen_size = screen.get_size()

        start_x = screen_size[0]*0.15
        start_y = screen_size[1]*0.1
        total_height = screen_size[1] * 0.8

        side_length = total_height//6
        for row in range(6):
            self.grid.append([])
            for col in range(6):
                self.grid[row].append(GridSquare(start_x + col * side_length, start_y + row * side_length, None, side_length=side_length))

        self.__get_symbols_bar(screen)
        return


    def __get_symbols_bar(self, screen):
        screen_size = screen.get_size()

        start_x = screen_size[0]*0.8
        side_length = screen_size[1]*0.8 // 6
        start_y = screen_size[1]*0.1 + side_length * 4

        x_box = GridSquare(start_x, start_y, 'X', side_length=side_length, highlighted=True)
        o_box = GridSquare(start_x, start_y+side_length, 'O', side_length=side_length)

        self.symbol_boxes = [x_box, o_box]

    def update_symbol(self, mpos):
        for box in self.symbol_boxes:
            if box.is_clicked(mpos):
                if box.highlighted == False:
                    box.highlighted = True
                    self.symbol_boxes[self.symbol_boxes.index(box)-1].highlighted = False
                return box.value
        return None

    def get_symbol(self):
        for box in self.symbol_boxes:
            if box.highlighted:
                return box.value

    def update_board(self, mpos):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                square = self.grid[row][col]
                if square.is_clicked(mpos):
                    square.value = self.get_symbol()
                    self.dict_representation[(row, col)] = square.value
                    return True
        return False

    def grid_from_dict(self, dict_representation):
        for key in dict_representation:
            row, col = key
            self.grid[row][col].update_value(dict_representation[key])
        self.dict_representation = dict_representation
        return

    def draw(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col].draw(screen)
        for box in self.symbol_boxes:
            box.draw(screen)



if __name__ == '__main__':
    screen = pygame.display.set_mode((720, 480))
    board = OrderAndChaosBoard(screen)
    board.draw(screen)
    cpu_player = (-1, 1)[random.randint(0,1)]
    print cpu_player
    done = False
    current_player = 1
    cpu_timelimit = 1
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                continue
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player != cpu_player:
                mpos = pygame.mouse.get_pos()
                board.update_symbol(mpos)
                if board.update_board(mpos):
                    current_player = (-1, 1)[ ~[-1, 1].index(current_player) ]

        state = OrderAndChaosState(board.dict_representation)
        if state.is_end_game:
            done = True
            if state.winning_player == cpu_player:
                print "CPU wins"
            else:
                print "You win"

        board.draw(screen)
        pygame.display.flip()

        if current_player == cpu_player:
            move = state.monte_next_move(num_games=50)
            board.grid_from_dict(move.state_grid)
            current_player = (-1, 1)[ ~[-1, 1].index(current_player) ]

        board.draw(screen)
        pygame.display.flip()
