import util
from search import aStarSearch

class Actions:
    NORTH = (0, 1)
    SOUTH = (0, -1)
    EAST = (1, 0)
    WEST = (-1, 0)
    HOLD = (0, 0)

def toVector(direction):
    return direction[0], direction[1]

class Player:
    
    def __init__(self, game_map, player_start, goal_state, patrol_starts, costFn=lambda x: 1):
        self.game_map = game_map
        self.player_start = player_start
        self.goal_state = goal_state
        self.patrol_starts = patrol_starts
        self.costFn = costFn

    def getStartState(self):
        return self.player_start

    def goalTest(self, state):
        return state == self.goal_state

    def getActions(self, state):
        actions = [Actions.HOLD]
        for action in [Actions.NORTH, Actions.SOUTH, Actions.EAST, Actions.WEST]:
            dx, dy = toVector(action)
            x, y = state[0]+dx, state[1]+dy
            if not self.game_map[x][y]:
                actions.append(action)
        return actions

    def getResult(self, state, action):
        dx, dy = toVector(action)
        x, y = state[0]+dx, state[1]+dy
        if self.game_map[x][y]:
            print("Invalid state!")
            return state
        return (x, y)

    def getCost(self, state, action):
        nextState = self.getResult(state, action)
        if nextState == state:
            return 0
        return self.costFn(nextState)

    def getCostOfActions(self, actions):
        if actions == None: 
            return float('inf')
        state = self.getStartState()
        cost = 0
        for action in actions:
            dx, dy = toVector(action)
            x, y = state[0]+dx, state[1]+dy
            # Check figure out the next state and see whether its' legal
            if self.game_map[x][y]: 
                return float('inf')
            cost += self.costFn((x, y))
        return cost

    def getNextStep(self):
        return aStarSearch(self)[1]