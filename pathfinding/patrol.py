from util import Actions, toVector
from search import aStarSearch

class Patrol:
    
    def __init__(self, game_map, patrol_start, last_known_player_position):
        self.game_map = [[-1]*len(game_map[1]) for i in range(len(game_map))]
        self.true_map = game_map
        self.patrol_start = patrol_start
        self.last_known_player_position = last_known_player_position
        x, y = patrol_start
        self.explore(x, y)

    def explore(self, x, y):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                self.game_map[i][j] = self.true_map[i][j]

    def getStartState(self):
        return self.patrol_start

    def goalTest(self, state):
        return state == self.last_known_player_position

    def getActions(self, state):
        actions = [Actions.HOLD]
        for action in [Actions.NORTH, Actions.SOUTH, Actions.EAST, Actions.WEST]:
            dx, dy = toVector(action)
            x, y = state[0]+dx, state[1]+dy
            if self.game_map[x][y] < 1:
                actions.append(action)
        return actions

    def getResult(self, state, action):
        dx, dy = toVector(action)
        x, y = state[0]+dx, state[1]+dy
        if self.game_map[x][y] > 0:
            print("Invalid state!")
            return state
        return (x, y)

    def getCost(self, state, action):
        nextState = self.getResult(state, action)
        if nextState == state:
            return 0
        return 1

    def getCostOfActions(self, actions):
        if actions == None: 
            return float('inf')
        state = self.getStartState()
        cost = 0
        for action in actions:
            dx, dy = toVector(action)
            x, y = state[0]+dx, state[1]+dy
            if self.game_map[x][y] > 0: 
                return float('inf')
            cost += 1
        return cost

    def getNextStep(self):
        path = aStarSearch(self)
        if len(path) == 0:
            return path[0]
        return path[1]

    def update(self, patrol_state, patrol_states):
        self.patrol_start = patrol_state
        x, y = patrol_state
        self.explore(x, y)