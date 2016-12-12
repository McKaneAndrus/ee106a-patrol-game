from player import Player

game_map = [[1, 1, 1, 1, 1],[1, 0, 0, 0, 1],[1, 0, 2, 1, 1],[1, 0, 0, 0, 1],[1, 1, 1, 1, 1]]
start = (1, 2)
goal = (3, 2)
player = Player(game_map, start, goal, [])

next_step = player.getNextStep()
print(next_step)