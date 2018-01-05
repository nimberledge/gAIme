import pickle
class GameLogger(object):

    def __init__(self):
        pass

    def log_game(self, write_file):
        """
        Stores game states in the file sequentially.
        """
        output = open(write_file, 'wb')
        for gameState in self:
            pickle.dump(gameState, output, pickle.HIGHEST_PROTOCOL)
        output.close()
    def log_state(self, game_state, write_file):
        """
        Appends the game_state to the write_file
        """
        output = open(write_file, 'wb')
        pickle.dump(game_state, output, pickle.HIGHEST_PROTOCOL)
        output.close()
    def get_game(self, read_file):
        """
        Reads the read_file and returns a list of game state objects in the order that they were put into the file.
        """
        input = open(read_file, 'rb')
        result = []
        notEmpty = True
        while (notEmpty):
            result.append(pickle.load(read_file))
        input.close()
        return result
    def get_state(self, read_file, position=0):
        """
        Returns the game state object at the given position
        """
        gameStateList = self.get_game(read_file)
        return gameStateList[position]