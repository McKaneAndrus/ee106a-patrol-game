#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import Bool
from game2 import get_map_dims, reveal  #, get_coord, get_orientation
from zumy_controller2 import ZumyController
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker
from util import Actions, to_vector
from search import aStarSearch, manhattanHeuristic
import copy
import time
import threading

class Patrol:
    
    def __init__(self, zumy, tag, player_tag, other_patrol_zumy, other_patrol_tag, side_tags, map_dims):
        self.controller = ZumyController(zumy, tag)
        self.game_map = [[-1]*map_dims[1] for i in range(map_dims[0])]
        print self.print_map()
        self.patrol_state = self.controller.get_state()
        self.player_tag = player_tag
        self.player_sidetags = side_tags
        self.lkpp = (1,1)
        self.nearest_pos = None
        # self.lock = threading.RLock()
        self.interrupt = [False]
        self.end = threading.Event()
        self.pause = threading.Event()
        self.pause.set()
        self.end.set()
        self.observations = 0
        self.alpha = 0.1
        self.cam_checker = rospy.Subscriber(zumy + "/ar_pose_marker", AlvarMarkers, self.check_fov)
        self.winner = False
        self.win_broadcaster = rospy.Publisher("patrol_" + tag + "_won", Bool, queue_size=2)

        # self.other_cam_checker = rospy.Subscriber(other_patrol_zumy + "/ar_pose_marker", AlvarMarkers, self.check_others_fov)
        self.other_patrol = other_patrol_tag
        self.other_patrol_won = rospy.Subscriber("patrol_" + other_patrol_tag + "_won", Bool, self.other_won_callback)
        self.other_patrol_state = self.controller.get_coord_of(self.other_patrol)

        self.player_won = rospy.Subscriber("player_won", Bool, self.player_won_callback)
        self.game_over = False

    def other_won_callback(self, msg):
        if msg.data:
            # self.lock.acquire()
            self.end.clear()
            # print "Patrols won!"
            self.winner = True
            self.game_over = True
            self.interrupt[0] = True
            self.end.set()
            # self.lock.release()

        
    def player_won_callback(self, msg):
        if msg.data:
            # self.lock.acquire()
            self.end.clear()
            # print "Player won D:"
            self.winner = False
            self.game_over = True
            self.interrupt[0] = True
            self.end.set()
            # self.lock.release()
        else:
            self.end.clear()
            # print "Player lost!:"
            self.winner = True
            self.game_over = True
            self.interrupt[0] = True
            self.end.set()

    def check_fov(self, msg):
        observed = False
        # print "++++++++++++++++++++++++++FOVING++++++++++++++++++++++++++"
        for marker in msg.markers:
            # print marker.id, self.player_sidetags
            if str(marker.id) in self.player_sidetags:
                # print "updating lkpp because of fov"
                self.lkpp = self.controller.get_coord_of(self.player_tag)
                # print "Player at", self.lkpp
                observed = True
        if observed:
            self.observations = self.observations * (1 - self.alpha) + self.alpha
        else:
            self.observations = self.observations * (1 - self.alpha)
        # print "obs", self.observations
        if self.observations > 0.8:
            # self.lock.acquire()
            self.end.clear()
            self.game_over = True
            self.winner = True
            self.interrupt[0] = True
            self.end.set()
            # self.lock.release()
        elif self.observations > 0.2:
            self.pause.clear()
            self.interrupt[0] = True
            self.pause.set()
        elif self.interrupt[0] and not self.game_over:
            self.interrupt[0] = False

    # def check_others_fov(self, msg):
    #     for marker in msg.markers:
    #         if str(marker.id) in self.player_sidetags:
    #             print "updating lkpp because of other"
    #             self.lkpp = self.controller.get_coord_of(self.player_tag)
    #             print "Player at", self.lkpp

    def explore(self):
        # print "exploring"
        curr_loc = self.patrol_state[0]
        # print "curr loc", curr_loc

        for loc in reveal(*curr_loc):
            if self.game_map[loc[0]][loc[1]] == -1:
                # print "adding", loc
                self.game_map[loc[0]][loc[1]] = loc[2]
        print self.print_map()


    def ping(self):
        print "updating lkpp because of ping"
        self.lkpp = self.controller.get_coord_of(self.player_tag)
        print "Player at", self.lkpp

    def find_closest_point(self):
        if self.game_map[self.lkpp[0]][self.lkpp[1]] == 0:
            return self.lkpp

        best = ((-1,-1), float('inf'))
        for x in range(len(self.game_map)):
            for y in range(len(self.game_map[0])):
                if self.game_map[x][y] == 0 and (x,y) != self.patrol_state[0] and (x,y) != self.other_patrol_state:
                    # print self.patrol_state[0], self.lkpp
                    explore_val = 0.1 * sum([self.game_map[loc[0]][loc[1]] for loc in reveal(x,y) if self.game_map[loc[0]][loc[1]] == -1])
                    pos_dist = ((x,y),manhattanHeuristic((x,y), self.lkpp) + explore_val)
                    # print pos_dist, self.patrol
                    best = min(best, pos_dist, key=lambda k: k[1])
        return best[0] if best[0] != (-1,-1) else self.patrol_state[0]


    def getStartState(self):
        return self.patrol_state[0]

    def goalTest(self, state):
        return state == self.nearest_pos

    def blocked(self, x, y):
        if x < len(self.game_map) and y < len(self.game_map[0]):
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
            cost += 1
        return cost

    def update_other_patrol(self):
        self.other_patrol_state = self.controller.get_coord_of(self.other_patrol)

    def print_map(self):
        print ""
        for y in reversed(range(len(self.game_map[0]))):
            for x in range(len(self.game_map)):
                print self.game_map[x][y], " ",
            print " "

    def get_next_step(self):
        print "obs", self.observations
        if self.observations > 0.2:
            print "gonna keep staring at this view"
            return self.patrol_state[0]
        self.update_other_patrol()
        self.nearest_pos = self.find_closest_point()
        print "pathing to ", self.nearest_pos
        path = aStarSearch(self, self.nearest_pos)
        print path
        if len(path) == 1:
            print("Nowhere to go")
            return path[0]
        return path[1]

    # def update_patrols(self):
    #     self.patrol_states = [(self.controller.get_coord_of(tag), self.controller.get_orientation_of(tag)) for tag in self.patrol_tags]

    def update(self, ping=False):
        self.explore()
        if ping:
            self.ping()
        waypoint = self.get_next_step()
        self.controller.go_to_waypoint(waypoint, self.interrupt)

        self.patrol_state = self.controller.get_state()
    
if __name__=='__main__':
    if len(sys.argv) < 6:
        print('Use: zumy_patrol.py [ zumy name ] [ zumy tag ], [ player tag ], [ other patrol zumy ], [ other patrol tag ] [tag on side] ...')
        sys.exit()

    rospy.init_node(sys.argv[1] + "_patrol")

    patrol = Patrol(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6:], get_map_dims())


    next_pulse = time.time()

    #rospy.Subscriber(sys.argv[1] + "/ar_pose_marker", AlvarMarkers, lambda msg: patrol.seen_callback(msg, i))

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown() and not patrol.game_over:
        try:
            ping = False
            if time.time() > next_pulse:
                next_pulse = time.time() + 5.0
                ping = True
            # patrol.lock.acquire()
            patrol.update(ping=ping)
            patrol.end.wait()
            patrol.pause.wait()
            # patrol.lock.release()
        except rospy.ROSInterruptException: 
            pass
        rate.sleep()

    if patrol.winner:
        print "Patrols won!"
    else:
        print "Player won TT_TT"
    end = rospy.get_time() + 2
    while not rospy.is_shutdown() and rospy.get_time() < end:
        if patrol.winner:
            patrol.win_broadcaster.publish(Bool(True))
