#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import Bool
from game2 import get_map  #, get_coord, get_orientation
from zumy_controller2 import ZumyController
from util import Actions, to_vector
from search import aStarSearch, manhattanHeuristic
import threading
import copy
import time

class Player:
    
    def __init__(self, zumy, tag, patrol_tags, game_map):
        self.controller = ZumyController(zumy, tag)
        self.true_map = game_map
        self.player_state = self.controller.get_coord()
        self.goal_state = self.find_goal()

        self.end = threading.Event()
        self.end.set()
        self.interrupt = [False]

        self.patrol_tags = patrol_tags
        self.patrol_states = []
        self.update_patrols()
        # print "gonna make a map"
        self.game_map = copy.deepcopy(self.true_map)
        self.rebuild_game_map()

        self.patrol_1_won = rospy.Subscriber("patrol_" + patrol_tags[0] + "_won", Bool, self.patrol_won_callback)
        self.patrol_2_won = rospy.Subscriber("patrol_" + patrol_tags[1] + "_won", Bool, self.patrol_won_callback)

        self.winner = False
        self.win_broadcaster = rospy.Publisher("player_won", Bool, queue_size=2)
        self.game_over = False

    def patrol_won_callback(self, msg):
        if msg.data:
            self.end.clear()
            # print "Patrols won!"
            self.winner = False
            self.game_over = True
            self.interrupt[0] = True
            self.end.set()

    def find_goal(self):
        for i in range(len(self.true_map)):
            for j in range(len(self.true_map[0])):
                if self.true_map[i][j] == 9:
                    return (i, j)

    def rebuild_game_map(self):
        # print "rebuilding map", self.game_map, "\n\n", self.true_map

        self.update_patrols()
        self.game_map = copy.deepcopy(self.true_map)
        for patrol in self.patrol_states:
            print "Patrol:", patrol
            x, y = patrol[0]
            dx, dy = patrol[1]
            self.game_map[x][y] = 1
            # print "checking", (x+dx, y+dy)
            while not self.blocked(x+dx, y+dy): # self.game_map[x+dx][y+dy] :
                x += dx
                y += dy
                # print "invalidating: ", (x,y)
                self.game_map[x][y] = 1
                # print "checking", (x+dx, y+dy)
        print "Map: ", self.print_map()

    def getStartState(self):
        return self.player_state

    def goalTest(self, state):
        return state == self.goal_state

    def blocked(self, x, y):
        if x < len(self.game_map) and y < len(self.game_map[0]) and x >= 0 and y >= 0:
            return self.game_map[x][y] != 0 and self.game_map[x][y] != 9
        return True
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
            for patrol in self.patrol_states:
                cost += 1 + 1.0/(10 * manhattanHeuristic((x,y), patrol[0]))
        return cost

    def get_next_step(self):
        path = aStarSearch(self, self.goal_state)
        print path
        if len(path) == 1:
            options = [self.getResult(self.player_state, action) for action in self.getActions(self.player_state)] + [self.player_state]
            best = max(options, key = lambda opt: sum([manhattanHeuristic(opt, patrol[0]) for patrol in self.patrol_states]))
            print best
            return best
        return path[1]

    def print_map(self):
        print ""
        for y in reversed(range(len(self.game_map[0]))):
            for x in range(len(self.game_map)):
                print self.game_map[x][y], " ",
            print " "


    def update_patrols(self):
        self.patrol_states = [(self.controller.get_coord_of(tag), self.controller.get_orientation_of(tag)) for tag in self.patrol_tags]
        for state in self.patrol_states:
            print (state[0][0] + state[0][1], state[1][0] + state[1][1]), self.player_state
            if (state[0][0] + state[1][0], state[0][1] + state[1][1]) == self.player_state:
                self.end.clear()
                # print "Patrols won!"
                self.winner = False
                self.game_over = True
                self.interrupt[0] = True
                self.end.set()

    def act(self):
        print "acting"
        self.rebuild_game_map()
        waypoint = self.get_next_step()
        print "going to ", waypoint
        self.controller.go_to_waypoint(waypoint, self.interrupt)
        self.player_state = self.controller.get_coord()
        if self.goalTest(self.player_state):
            self.end.clear()
            # print "Patrols won!"
            self.winner = True
            self.game_over = True
            self.interrupt[0] = True
            self.end.set()
    
if __name__=='__main__':
    if len(sys.argv) < 4:
        print('Use: zumy_player.py [ zumy name ] [ zumy tag ] [ patrol1 tag ] ...')
        sys.exit()
    # print "initialize?"
    rospy.init_node('zumy_%s' % sys.argv[1])
    # print "initialized?"


    if len(sys.argv) < 3:
        patrols = []
    else:
        patrols = sys.argv[3:]
    # print "gonna make a player"
    player = Player(sys.argv[1], sys.argv[2], patrols, get_map())
    # print "made player"
    rate = rospy.Rate(10.0)
    # print "entering?"
    while not rospy.is_shutdown() and not player.game_over:
        # print "gonna try to act"
        player.end.wait()
        try:
            player.act()
        except rospy.ROSInterruptException:
            pass
        rate.sleep()


    end = time.time() + 10
    while not rospy.is_shutdown() and time.time() < end:
        if player.winner:
            player.win_broadcaster.publish(Bool(True))
        else:
            player.win_broadcaster.publish(Bool(False))