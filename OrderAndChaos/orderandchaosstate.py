from basegamestate import BaseGameState
import time
import random

class OrderAndChaosState(BaseGameState):

    def __init__(self, board_grid, parent=None, children=None):
        self.state_grid = board_grid
        self.__moves_made = None
        agg_fn = (max, min)[self.moves_made % 2]
        super(OrderAndChaosState, self).__init__(parent=parent, children=children, agg_fn=agg_fn)
        self.__children = None
        self.string_rep = ''
        self._static_score = None
        self._monte_carlo_moveset = None

    @property
    def moves_made(self):
        if self.__moves_made:
            return self.__moves_made

        moves_made = 0
        for grid_square in self.state_grid:
            if self.state_grid[grid_square] is not None:
                moves_made += 1

        self.__moves_made = moves_made
        return self.__moves_made

    @property
    def children(self):
        if self.__children:
            return self.__children

        self.__children = []
        temp_grid = dict(self.state_grid)

        for key in temp_grid:

            if temp_grid[key] is None:
                temp_grid[key] = 'X'
                child = OrderAndChaosState(dict(temp_grid), parent=self)
                self.__children.append(child)

                temp_grid[key] = 'O'
                child = OrderAndChaosState(dict(temp_grid), parent=self)
                self.__children.append(child)

                temp_grid = dict(self.state_grid)
        return self.__children


    @property
    def monte_carlo_moveset(self, max_moves=50):
        if self._monte_carlo_moveset:
            return self._monte_carlo_moveset

        moves_left = 2 * len([1 for i in self.state_grid if self.state_grid[i] is None])
        self._monte_carlo_moveset = []
        indexes = {}
        moves = []
        while len(indexes) < min(max_moves, moves_left):
            index = random.randint(0, len(self.children)-1)
            if index in indexes:
                continue
            self._monte_carlo_moveset.append(self.children[index])
            indexes[index] = True
        return self._monte_carlo_moveset

    def make_random_move(self):
        for key in self.state_grid:
            if self.state_grid[key] is None:
                sym = ('O', 'X')[random.randint(0,1)]
                temp_grid = dict(self.state_grid)
                temp_grid[key] = sym
                child = OrderAndChaosState(temp_grid)
                return child

    @property
    def is_end_game(self):
        if self.moves_made < 5:
            return False
        if self.static_score >= 5:
            return True
        if self.moves_made >= 36:
            return True
        return False

    @property
    def winning_player(self):
        if self.static_score >= 5:
            return 1
        return -1

    @property
    def static_score(self):
        if self._static_score:
            return self._static_score

        visited = {}
        max_count = 0
        for key in self.state_grid:
            if self.state_grid[key] is None:
                continue

            row, col = key
            symbol = self.state_grid[key]
            t_row, t_col = row, col
            # print (t_row, t_col)
            counter = 1
            while (t_row < 5):  #Just down
                t_row += 1
                if self.state_grid[(t_row, t_col)] == symbol:
                    counter += 1
                else:
                    break
            if counter > max_count:
                max_count = counter

            t_row, t_col = row, col
            counter = 1

            while (t_row > 0):  #Just up
                t_row -= 1
                if self.state_grid[(t_row, t_col)] == symbol:
                    counter += 1
                else:
                    break
            if counter > max_count:
                max_count = counter

            t_row, t_col = row, col
            counter = 1

            while (t_col > 0):  #Just left
                t_col -= 1
                if self.state_grid[(t_row, t_col)] == symbol:
                    counter += 1
                else:
                    break
            if counter > max_count:
                max_count = counter

            t_row, t_col = row, col
            counter = 1

            while (t_col < 5):  #Just right
                t_col += 1
                if self.state_grid[(t_row, t_col)] == symbol:
                    counter += 1
                else:
                    break
            if counter > max_count:
                max_count = counter

            t_row, t_col = row, col
            counter = 1

            while (t_row > 0 and t_col > 0):  #Up right
                t_row -= 1
                t_col -= 1
                if self.state_grid[(t_row, t_col)] == symbol:
                    counter += 1
                else:
                    break
            if counter > max_count:
                max_count = counter

            t_row, t_col = row, col
            counter = 1

            while (t_row > 0 and t_col < 5):  #Down right
                t_row -= 1
                t_col += 1
                if self.state_grid[(t_row, t_col)] == symbol:
                    counter += 1
                else:
                    break
            if counter > max_count:
                max_count = counter

            t_row, t_col = row, col
            counter = 1

            while (t_row > 0 and t_col < 5):  #Down left
                t_row -= 1
                t_col += 1
                if self.state_grid[(t_row, t_col)] == symbol:
                    counter += 1
                else:
                    break
            if counter > max_count:
                max_count = counter

            t_row, t_col = row, col
            counter = 1

            while (t_row > 0 and t_col > 0):  #Up left
                t_row -= 1
                t_col -= 1
                if self.state_grid[(t_row, t_col)] == symbol:
                    counter += 1
                else:
                    break
            if counter > max_count:
                max_count = counter
        if max_count >= 5:
            self._static_score = 10**9
        else:
            self._static_score = max_count
        return self._static_score

    def __str__(self):
        if self.string_rep:
            return self.string_rep

        count = 0
        keys = self.state_grid.keys()
        keys.sort()
        for key in keys:
            if self.state_grid[key]:
                self.string_rep += self.state_grid[key] + ' '
            else:
                self.string_rep += '* '
            count += 1
            if count % 6 == 0:
                self.string_rep += '\n'

        return self.string_rep


if __name__ == '__main__':
    test = {
        (0, 0): None,
        (0, 1): None,
        (0, 2): None,
        (0, 3): None,
        (0, 4): None,
        (0, 5): None,
        (1, 0): None,
        (1, 1): None,
        (1, 2): None,
        (1, 3): None,
        (1, 4): None,
        (1, 5): None,
        (2, 0): None,
        (2, 1): None,
        (2, 2): None,
        (2, 3): None,
        (2, 4): None,
        (2, 5): None,
        (3, 0): None,
        (3, 1): None,
        (3, 2): None,
        (3, 3): None,
        (3, 4): None,
        (3, 5): None,
        (4, 0): None,
        (4, 1): None,
        (4, 2): None,
        (4, 3): None,
        (4, 4): None,
        (4, 5): None,
        (5, 0): None,
        (5, 1): None,
        (5, 2): None,
        (5, 3): None,
        (5, 4): None,
        (5, 5): None,
    }
    test_state = OrderAndChaosState(test)
    print test_state
    print test_state.static_score
    term = time.time() + 1
    i = 1
    while time.time() < term:
        move = test_state.next_move(i, termination_time=term)
        i += 1
    print move
