#!/usr/bin/env python
import rospy
import sys
import time

from ar_track_alvar_msgs.msg import AlvarMarkers

from util import Actions, to_vector
from search import aStarSearch
from zumy_controller import ZumyController
from game2 import get_coord, reveal, get_map_dims

class Patrol:
    
    def __init__(self, zumy, tag, player_tag, map_dims):
        self.controller = ZumyController(zumy, tag)
        self.game_map = [[-1]*map_dims[1] for i in range(map_dims)]
        
        self.patrol_state = self.controller.get_state()
        self.player_tag = player_tag
        self.last_known_player_position = None
        self.ping()

        x, y = self.patrol_state[0]
        self.explore(x, y)

    def explore(self, x, y):
        for loc in reveal(x, y):
			self.game_map[loc[0]][loc[1]] = loc[2]

	def ping(self):
		self.last_known_player_position = get_coord(self.player_tag)

    def getStartState(self):
        return self.patrol_state[0]

    def goalTest(self, state):
        return state == self.last_known_player_position

    def getActions(self, state):
        actions = []
        for action in [Actions.NORTH, Actions.SOUTH, Actions.EAST, Actions.WEST]:
            dx, dy = to_vector(action)
            x, y = state[0]+dx, state[1]+dy
            if self.game_map[x][y] < 1:
                actions.append(action)
        return actions

    def getResult(self, state, action):
        dx, dy = to_vector(action)
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
            dx, dy = to_vector(action)
            x, y = state[0]+dx, state[1]+dy
            if self.game_map[x][y] > 0: 
                return float('inf')
            cost += 1
        return cost

    def get_next_step(self):
        path = aStarSearch(self)
        if len(path) == 0:
            return path[0]
        return path[1]

    def update(self, ping=False):
        if ping:
            self.ping()
        waypoint = self.get_next_step()
        self.controller.go_to_waypoint(waypoint)

        self.patrol_state = self.controller.get_state()

    #def seen_callback(self, msg):


if __name__=='__main__':
	if len(sys.argv) < 5:
		print('Use: zumy_patrol.py [ zumy name ] [ zumy tag ], [patrol_index], [ player tag ]')
		sys.exit()

    rospy.init_node('zumy_patrol%s' % (sys.argv[3]))

	patrol = Patrol(sys.argv[1], sys.argv[2], sys.argv[3], get_map_dims())

    next_pulse = 5.

    #rospy.Subscriber(sys.argv[1] + "/ar_pose_marker", AlvarMarkers, lambda msg: patrol.seen_callback(msg, i))

	rate = rospy.Rate(10.0)
	while not rospy.is_shutdown():
		try:
            ping = False
            if time.time() > next_pulse:
                next_pulse = time.time() + 5.
                ping = True
			patrol.update(ping=ping)
		except rospy.ROSInterruptException: 
			pass
		rate.sleep()



        'patrol%s' % (i)