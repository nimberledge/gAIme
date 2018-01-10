import abc
from abc import abstractmethod
import time
import random


class BaseGameState(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, parent=None, agg_fn=max, children=None):
        assert agg_fn in (max, min)
        self.__parent = parent
        if children:
            self._children = children
        else:
            self._children = []
        self._monte_carlo_moveset = []
        self.state_scores_cache = {}
        self.agg_fn = agg_fn

    @property
    def parent(self):
        """
        :return: the parent game state of the current state
        """
        return self.__parent

    @property
    @abstractmethod
    def children(self):
        """
        :return: list of game states immediately reachable from current state
        """
        pass

    @property
    @abstractmethod
    def is_end_game(self):
        """
        :return: boolean indicating whether or not given game state is a terminal game state
        """
        pass

    @property
    @abstractmethod
    def winning_player(self):
        """
        :return: returns the winning player -
        1  for starting player
        -1 for the second player
        0  for a tie
        """
        pass

    @property
    @abstractmethod
    def static_score(self):
        """
        :return: evaluation function - customize to your game
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        """
        :return: string value of self
        """
        raise NotImplementedError

    # Optional methods
    @property
    def monte_carlo_moveset(self):
        """
        Moveset for the Monte Carlo algorithm. Needs to be implemented to use Monte Carlo.
        :return: list of moves - preferably not exhaustive - for the Monte Carlo algorithm to choose from.
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Needs to be implemented to use Monte Carlo. Must not call self.children - that is expensive.
        :return: random gamestate reachable from current state. Must be a fast computation.
        """
        raise NotImplementedError

    def play_through_at_random(self):
        """
        :return: result of a game played at random starting from the self state.
        """
        if self.is_end_game:
            return self.winning_player

        child = self.make_random_move()
        return child.play_through_at_random()

    def monte_next_move(self, player=1, num_games=100):
        """
        Pass -1 as player if it is the second player.
        :return: suggested move according to Monte Carlo algorithm.
        """
        # Loop through all the moves in moveset
        successes = []
        moves = self.monte_carlo_moveset
        for child in moves:
            # Calculate success rate of each move
            success = 0
            for game in range(num_games):
                add = child.play_through_at_random()
                success += add

            success *= player  # Account for second player state, ie count wins correctly
            successes.append(success / num_games)

        # Pick the most successful
        return moves[successes.index(max(successes))]


    def dynamic_score(self, depth, termination_time=None):
        """
        :param depth: level of recursive depth to compute score
        :param termination_time: time (as an absolute system time) passed to halt execution. optional parameter
        :return: normalized minimax score of a state
        """
        assert depth >= 0
        if depth in self.state_scores_cache:
            return self.state_scores_cache[depth]

        if depth == 0:
            score = self.static_score
            self.state_scores_cache[depth] = score
            return score

        if not self.children:
            return self.static_score

        if termination_time:
            if time.time() > termination_time:
                return self.state_scores_cache[depth-1]

        children_scores = []
        for child in self.children:
            if termination_time and time.time() >= termination_time:
                return self.state_scores_cache[depth-1]
                # continue

            children_scores.append(child.dynamic_score(depth - 1, termination_time=termination_time))

        score = self.agg_fn(children_scores)
        self.state_scores_cache[depth] = score
        return self.state_scores_cache[depth]

    def next_move(self, depth, termination_time=None):
        """
        :param depth: level of recursive depth to compute move
        :param termination_time: time (as an absolute system time) passed to halt execution. optional parameter
        :return: suggested child of state to play
        """
        score = self.dynamic_score(depth, termination_time=termination_time)

        if not self.children:
            return None

        for child in self.children:

            if child.dynamic_score(depth-1, termination_time=termination_time) == score:
                return child

        # If it doesn't match any of its children, something has gone wrong. Play at random.
        return self.children[random.randint(0, len(self.children)-1)]


if __name__ == "__main__":
    pass
