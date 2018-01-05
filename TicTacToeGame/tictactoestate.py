from basegamestate import BaseGameState
import random

class TicTacToeState(BaseGameState):

    WIN_INDICE_LISTS = [[0, 1, 2],
                        [0, 3, 6],
                        [0, 4, 8],
                        [1, 4, 7],
                        [2, 5, 8],
                        [3, 4, 5],
                        [6, 7, 8],
                        [2, 4, 6]]

    def __init__(self, state_list, parent=None, children=None):
        self.state_list = state_list
        self.moves_so_far = sum([1 for el in self.state_list if el])
        self.current_player = self.moves_so_far % 2
        agg_fn = (min, max)[self.current_player]
        super(TicTacToeState, self).__init__(parent=parent, agg_fn=agg_fn, children=children)
        self.string_rep =''
        self._static_score = None

    @property
    def children(self):
        if self._children:
            return self._children

        if self.is_end_game:
            return []

        move = ('X', 'O')[self.current_player]

        for index in range(len(self.state_list)):
            if self.state_list[index] is None:
                temp_state = list(self.state_list)
                temp_state[index] = move
                self._children.append(TicTacToeState(temp_state))

        return self._children

    @property
    def monte_carlo_moveset(self, num_moves=4):
        if self._monte_carlo_moveset:
            return self._monte_carlo_moveset

        if self.is_end_game:
            self._monte_carlo_moveset = []

        move = ('X', 'O')[self.current_player]
        indices = []
        index = random.randint(0,8)

        for i in range(min(num_moves, 9 - self.moves_so_far)):
            while (self.state_list[index] is not None) or (index in indices):
                index = random.randint(0,8)
            temp_state = list(self.state_list)
            temp_state[index] = move
            self._monte_carlo_moveset.append(TicTacToeState(temp_state))
            indices.append(index)

        return self._monte_carlo_moveset


    @property
    def static_score(self):
        pass

    @property
    def state(self):
        return self.state_list

    @property
    def is_end_game(self):
        if self.moves_so_far == 9:
            return True

        for index_list in self.WIN_INDICE_LISTS:
            win_flag = True
            for each_index, each in enumerate(index_list):

                if not(self.state_list[each] and self.state_list[each] == self.state_list[index_list[each_index-1]]):
                    win_flag = False
                    break

            if win_flag:
                return True

        return False

    @property
    def winning_player(self):
        for index_list in self.WIN_INDICE_LISTS:
            win_flag = True
            for each_index, each in enumerate(index_list):

                if not(self.state_list[each] and self.state_list[each] == self.state_list[index_list[each_index-1]]):
                    win_flag = False
                    break

            if win_flag:
                sym = self.state_list[index_list[0]]
                if sym == 'X':
                    return 1
                return -1
        return 0



    def make_random_move(self):
        temp_state = list(self.state_list)
        move = ('X', 'O')[self.current_player]
        index = random.randint(0,8)

        while (self.state_list[index] is not None):
            index = random.randint(0,8)

        temp_state[index] = move
        child = TicTacToeState(temp_state)

        return child

    def __str__(self):
        if self.string_rep:
            return self.string_rep

        for row in range(3):
            for col in range(3):
                if self.state_list[3*row + col]:
                    self.string_rep += str(self.state_list[3*row + col])
                else:
                    self.string_rep += ' '

            self.string_rep += '\n'
        return self.string_rep

if __name__ == '__main__':
    test_obj = TicTacToeState(['X', 'O', None, 'X', 'O', 'X', None, None, None])
    L = ['X']
    L.extend([None for i in range(8)])
    test_obj2 = TicTacToeState(L)
    #print (test_obj, end='\n')
    #print ('\n'.join([str(child) for child in test_obj.monte_carlo_moveset]), end='')
    # print(test_obj2.is_end_game)
    # print(test_obj.is_end_game)
    # print(test_obj2.winning_player)
    print (test_obj2, end='')
    move = test_obj2.monte_next_move(player=-1)
    print (move, end='')
