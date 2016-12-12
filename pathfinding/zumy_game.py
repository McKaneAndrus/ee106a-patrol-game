from search import aStarSearch
from problems import playerProblem, patrolProblem

game_map = [[1, 1, 1, 1, 1],[1, 0, 0, 0, 1],[1, 0, 1, 1, 1],[1, 0, 0, 0, 1],[1, 1, 1, 1, 1]]
start = (1, 2)
goal = (3, 2)
problem = playerProblem(game_map, start, goal, [])

steps = aStarSearch(problem)

print(steps)