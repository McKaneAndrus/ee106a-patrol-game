from player import Player

game_map = [[1, 1, 1, 1, 1, 1, 1],
			[1, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 1],
			[1, 0, 1, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 1],
			[1, 1, 1, 1, 1, 1, 1]]
start = (1, 1)
goal = (4, 5)
patrol = ((3, 4), (0, -1))
player = Player(game_map, start, goal, [patrol])

next_step = player.getNextStep()
print(next_step)