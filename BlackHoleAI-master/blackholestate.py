from basegamestate import BaseGameState
from boardentry import BoardEntry
import random

class BlackHoleState(BaseGameState):

    # Map of neighbours
    N_MAP = {
        1: (2, 3),
        2: (1, 3, 4, 5),
        3: (1, 2, 5, 6),
        4: (2, 5, 7, 8),
        5: (2, 3, 4, 6, 8, 9),
        6: (3, 5, 9, 10),
        7: (4, 8, 11, 12),
        8: (4, 5, 7, 9, 12, 13),
        9: (5, 6, 8, 10, 13, 14),
        10: (6, 9, 14, 15),
        11: (7, 12, 16, 17),
        12: (7, 8, 11, 13, 17, 18),
        13: (8, 9, 12, 14, 18, 19),
        14: (9, 10, 13, 15, 19, 20),
        15: (10, 14, 20, 21),
        16: (11, 17),
        17: (11, 12, 16, 18),
        18: (17, 12, 13, 19),
        19: (18, 13, 14, 20),
        20: (19, 14, 15, 21),
        21: (20, 15)
    }

    def __init__(self, state_list, parent=None, children=None):
        self.state_list = state_list
        self.moves_so_far = sum([1 for index in range(len(self.state_list)) if self.state_list[index]])
        self.current_player = self.moves_so_far % 2
        agg_fn = (min, max)[self.current_player]
        super(BlackHoleState, self).__init__(parent=parent, agg_fn=agg_fn, children=children)
        self.string_rep = ''
        self._static_score = None

    @property
    def children(self):
        if self._children:
            return self._children

        if self.moves_so_far == 20:
            self._children = []
            return self._children

        move_tuple = BoardEntry(self.moves_so_far//2 + 1, self.moves_so_far % 2)

        temp_state = list(self.state_list)

        for index in range(len(self.state_list)):
            if self.state_list[index] is None:
                temp_state[index] = move_tuple
                child = BlackHoleState(temp_state)
                self._children.append(child)
                temp_state = list(self.state_list)

        return self._children

    @property
    def monte_carlo_moveset(self, num_moves=20):
        """
        :return: list of moves at most num_moves -not exhaustive - for the Monte Carlo algorithm to choose from.
        """
        if self._monte_carlo_moveset:
            return self._monte_carlo_moveset
        moves = []

        if self.moves_so_far == 20:
            self._children = []
            return self._children

        move_tuple = BoardEntry(self.moves_so_far//2 + 1, self.moves_so_far % 2)
        index = random.randint(0,20)
        indices = []
        temp_state = list(self.state_list)

        for i in range(min(num_moves, 20 - self.moves_so_far)):

            while (self.state_list[index] is not None or index in indices):
                index = random.randint(0,20)

            temp_state[index] = move_tuple
            child = BlackHoleState(temp_state)
            moves.append(child)
            temp_state = list(self.state_list)
            indices.append(index)

        self._monte_carlo_moveset = moves
        return self._monte_carlo_moveset

    def make_random_move(self):
        """
        :return: random gamestate reachable from current state. Must be a fast computation.
        """
        temp_state = list(self.state_list)
        move_tuple = BoardEntry(self.moves_so_far//2 + 1, self.moves_so_far % 2)
        index = random.randint(0,20)

        while (self.state_list[index] is not None):
            index = random.randint(0,20)

        temp_state[index] = move_tuple
        child = BlackHoleState(temp_state)

        return child

    @property
    def static_score(self):
        if self._static_score:
            return self._static_score

        sum_exposed_first_player = 0
        sum_exposed_second_player = 0

        for index in range (len(self.state_list)):
            entry = self.state_list[index]
            if entry is not None:

                if entry.player == 0:
                    for nbr in self.N_MAP[index+1]:
                        if self.state_list[nbr-1] is None:
                            sum_exposed_first_player += entry.value
                            break

                if entry.player == 1:
                    for nbr in self.N_MAP[index+1]:
                        if self.state_list[nbr-1] is None:
                            sum_exposed_second_player += entry.value
                            break

        self._static_score = sum_exposed_first_player - sum_exposed_second_player
        return self._static_score

    @property
    def state(self):
        return self.state_list

    @property
    def is_end_game(self):
        return sum([1 for index in range(len(self.state_list)) if self.state_list[index]]) == 20
    @property
    def winning_player(self):
        if not self.is_end_game:
            return None
        if self.static_score == 0: # Tie
            return 0
        if self.static_score > 0: # Player 2 wins
            return -1
        return 1  # Player 1 wins

    def __str__(self):
        if self.string_rep:
            return self.string_rep
        for ind, tup in enumerate(self.state_list):
            self.string_rep += str(ind+1) + ': ' + str(tup).lstrip('BoardEntry') + '\n'
        return self.string_rep

if __name__ == "__main__":
    sample_state = [None for index in range(21)]
    test_obj = BlackHoleState(sample_state)
    for i in test_obj.monte_carlo_moveset:
        print (i)
        # print (i.make_random_move())

    print ('\n\n')
    print (test_obj.monte_next_move())
