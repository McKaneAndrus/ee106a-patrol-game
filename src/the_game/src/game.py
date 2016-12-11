#!/usr/bin/env python
import tf
import rospy
import sys
import math
import numpy as np
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Transform, Vector3, Twist
from the_game.msg import Vector2
import exp_quat_func as eqf
import ar_tag_subs as ats
import time

global last_pulse, observations, game_over



def player_pos_callback(msg):
	global last_pulse
	if not last_pulse:
		next_pulse = time.time() + 5
	elif time.time() > next_pulse:
		radar.publish(msg)

def pos_callback(msg, patrol_pub):
	vectors = []
	for i in range(msg.x - 1, msg.x + 2):
		if i >= 0 and i <= len(grid_map):
			for j in range(msg.y - 1, msg.y + 2):
				if j >= 0 and j <= len(grid_map[0]):
					vectors += Vector3(i, j, grid_map[j][i])
	patrol_pub.publish(vectors)

def seen_callback(msg, patrol):
	observations[i] += [msg]
	if len(observations) > 100:
		if sum(observations) > 50:
			game_state.publish(False)
		else:
			observations[i] = []

if __name__=='__main__':
    if len(sys.argv) < 5 or len(sys.argv) % 2 != 1:
        print('Use: zumy_patrol.py [ player zumy ] [ player tag ] [ p1 zumy ] [ p1 tag ] [ p2 zumy ] [ p2 tag ] ...')
        sys.exit()
    rospy.init_node('game')
    radar = rospy.Publisher("radar", Vector2, queue_size = 1)

    grid_map = [[0,1,0,1,0,0,1,0,0,1],
    			[0,0,0,0,0,0,0,0,1,1],
    			[0,1,0,1,0,0,1,0,1,0],
    			[0,1,0,1,1,1,1,0,0,0],
    			[0,0,0,0,0,0,0,0,1,1],
    			[0,1,0,1,0,1,1,0,0,0],
    			[1,1,0,1,0,0,1,0,0,1]]
    game_state = rospy.Publisher("game_state", Bool, queue_size = 1)
    game_state.publish(False)

    ar_tags[sys.argv[1]] = "ar_marker_" + sys.argv[2]
    rospy.Subscriber("player_pos", Vector2, player_pos_callback)
    patrols = [sys.argv[3]]
    ar_tags[sys.argv[3]] = "ar_marker_" + sys.argv[4]
    patrol1_update = rospy.Publisher(sys.argv[3] + "_update", Update, queue_size = 1)
    rospy.Subscriber(sys.argv[3] + "_pos", Vector2, lambda msg: pos_callback(msg, patrol1_update))
    
    if len(sys.argv) > 5:
    	patrols += [sys.argv[5]]
	    ar_tags[sys.argv[5]] = "ar_marker_" + sys.argv[6]
	    patrol2_update = rospy.Publisher(sys.argv[5] + "_update", Update, queue_size = 1)
	    rospy.Subscriber(sys.argv[5] + "_pos", Vector2, lambda msg: pos_callback(msg, patrol2_update))
	    
	    if len(sys.argv) > 7:
	    	patrols += [sys.argv[7]]
	    	ar_tags[sys.argv[7]] = "ar_marker_" + sys.argv[8]
	    	patrol3_update = rospy.Publisher(sys.argv[7] + "_update", Update, queue_size = 1)
	    	rospy.Subscriber(sys.argv[7] + "_pos", Vector2, lambda msg: pos_callback(msg, patrol3_update))
	
	for i in range(len(patrols)):
		observations += [[]]
		rospy.Subscriber(patrols[i] + "/seen", Bool, lambda msg: seen_callback(msg, i))
