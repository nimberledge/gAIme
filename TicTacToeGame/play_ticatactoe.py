import pygame
from board import TicTacToeBoard
from tictactoestate import TicTacToeState
from random import randint

def game_loop():
	pygame.init()
	screen = pygame.display.set_mode([720, 480])
	screen.fill((0,0,0))
	game_board = TicTacToeBoard(screen)

	cpu_player = -1
	toss = randint(1,2)  # Simulating biased coin flip
	if toss == 1:  # In this case, CPU starts
		cpu_state = TicTacToeState(game_board.state)
		cpu_player = 1
		state = cpu_state.monte_next_move(player=cpu_player)
		game_board.update_to_state(state.state_list)
	cpu_flag = 0
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
				continue
			elif event.type == pygame.MOUSEBUTTONDOWN and not cpu_flag:
				mpos = pygame.mouse.get_pos()
				if game_board.update_board(mpos):
					cpu_flag = cpu_flag ^ 1

		game_board.draw(screen)
		pygame.display.flip()
		end = TicTacToeState(game_board.state)
		if end.is_end_game:
			done = True
			break

		if cpu_flag:
			cpu_state = TicTacToeState(game_board.state)
			state = cpu_state.monte_next_move(player=cpu_player)
			game_board.update_to_state(state.state_list)
			cpu_flag = cpu_flag ^ 1

		game_board.draw(screen)
		end = TicTacToeState(game_board.state)
		if end.is_end_game:
			done = True
			break

		pygame.display.flip()

	if end.winning_player == cpu_player:
		print('CPU wins')
	elif end.winning_player != 0:
		print ('You win!')
	else:
		print ('Tie')



if __name__ == '__main__':
	game_loop()
