from util import Actions, toVector
from search import aStarSearch

class Player:
    
    def __init__(self, game_map, player_start, goal_state, patrol_states):
        self.player_start = player_start
        self.goal_state = goal_state
        self.patrol_states = patrol_states
        self.true_map = game_map
        self.game_map = self.buildGameMap()

    def buildGameMap(self):
        self.game_map = self.true_map
        for patrol in self.patrol_states:
            x, y = patrol[0]
            dx, dy = patrol[1]
            self.game_map[x][y] = 2
            while not self.game_map[x+dx][y+dy]:
                x += dx
                y += dy
                self.game_map[x][y] = 3

    def getStartState(self):
        return self.player_start

    def goalTest(self, state):
        return state == self.goal_state

    def getActions(self, state):
        actions = [Actions.HOLD]
        for action in [Actions.NORTH, Actions.SOUTH, Actions.EAST, Actions.WEST]:
            dx, dy = toVector(action)
            x, y = state[0]+dx, state[1]+dy
            if self.game_map[x][y] == 0:
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
        self.buildGameMap()
        path = aStarSearch(self)
        if len(path) == 1:
            print("Nowhere to go")
            return path[0]
        return path[1]

    def update(self, player_state, patrol_states):
        self.player_start = player_state
        self.patrol_states = patrol_states
        self.buildGameMap()
