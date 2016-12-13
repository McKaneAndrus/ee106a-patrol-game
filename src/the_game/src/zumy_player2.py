import sys
import rospy

from game2 import get_map, get_coord, get_orientation
from zumy_controller2 import ZumyController
from util import Actions, to_vector
from search import aStarSearch

class Player:
    
    def __init__(self, zumy, tag, patrol_tags, game_map):
        self.controller = ZumyController(zumy, tag)

        self.player_state = self.controller.get_coord()
        self.goal_state = self.find_goal()
        self.patrol_tags = patrol_tags
        self.patrol_states = []
        self.true_map = game_map
        self.game_map = self.buildGameMap()

    def find_goal(self):
        for i in range(len(self.true_map)):
            for j in range(len(self.true_map[0])):
                if self.true_map[i][j] == 9:
                    return (i, j)

    def rebuild_game_map(self):
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
        return self.player_state

    def goalTest(self, state):
        return state == self.goal_state

    def blocked(self, x, y):
        return self.game_map[x][y] != 0 and self.game_map[x][y] != 9

    def getActions(self, state):
        actions = []
        for action in [Actions.NORTH, Actions.SOUTH, Actions.EAST, Actions.WEST]:
            dx, dy = to_vector(action)
            x, y = state[0]+dx, state[1]+dy
            if not self.blocked(x, y):
                actions.append(action)
        return actions

    def getResult(self, state, action):
        dx, dy = to_vector(action)
        x, y = state[0]+dx, state[1]+dy
        if self.blocked(x, y):
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
            dx, dy = to_vector(action)
            x, y = state[0]+dx, state[1]+dy
            if self.blocked(x, y): 
                return float('inf')
            cost += 1
        return cost

    def get_next_step(self):
        path = aStarSearch(self)
        if len(path) == 1:
            print("Nowhere to go")
            return path[0]
        return path[1]

    def act(self):
        self.rebuild_game_map()
        waypoint = self.get_next_step()
        self.controller.go_to_waypoint(waypoint)

        self.player_state = self.controller.get_position()
        self.patrol_states = [(get_coord(tag), get_orientation(tag)) for tag in self.patrol_tags]
    
if __name__=='__main__':
    if len(sys.argv) < 4:
        print('Use: zumy_player.py [ zumy name ] [ zumy tag ] [ patrol1 tag ] ...')
        sys.exit()

    rospy.init_node('zumy_player')

    if len(sys.argv) < 3:
        patrols = []
    else:
        patrols = sys.argv[3:]

    player = Player(sys.argv[1], sys.argv[2], patrols, get_map())

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            player.act()
        except rospy.ROSInterruptException:
            pass
        rate.sleep()
