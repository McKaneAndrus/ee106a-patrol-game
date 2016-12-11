#!/usr/bin/env python
import tf
import rospy
import sys
import math
import numpy as np
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Transform, Vector3, Twist
from the_game.msg import Vector2, Update
import exp_quat_func as eqf
import ar_tag_subs as ats
import zumy_controller
import random

global grid_map, player_position, game_over, invalid_path

def patrol(controller):
	global invalid_path

	path, invalid_path = astar(controller.get_coord(), player_position), False
	for node in path:
		if invalid_path:
			break
		controller.go_to_waypoint(node)

def astar(start, end):
	direction = 4 * random.random()
	if direction > 3:
		if not grid_map[start[1] + 1][start[0]]:
			return [(start[1] + 1), (start[0])]
	elif direction > 3:
		if not grid_map[start[1]-1][start[0]]:
			return [(start[1] - 1), (start[0])]
	elif direction > 3:
		if not grid_map[start[1]][start[0]+1]:
			return [(start[1]), (start[0]+1)]
	else:
		if not grid_map[start[1]][start[0] - 1]:
			return [(start[1]), (start[0] - 1)]

def game_callback(msg):
	global game_over
	game_over = msg

def nearby_callback(msg):
	global grid_map, invalid_path
	for vector in msg.Vectors:
		grid_map[vector.x][vector.y] = vector.z
	invalid_path = True

def radar_callback(msg):
	global player_position
	player_position = (msg.x, msg.y)


if __name__=='__main__':
    if len(sys.argv) < 5:
        print('Use: zumy_patrol.py [ zumy name ] [ zumy tag ] [ grid_x ] [ grid_y ]')
        sys.exit()
    rospy.init_node('zumy_patrol_{}' + sys.argv[1])
    controller = Zumy_Controller(sys.argv[1], sys.argv[2])
    grid_map = [[2] * sys.argv[2]] * sys.argv[3]

    rospy.Subscriber("game_state", Bool, game_callback)
    pos_pub = rospy.Publisher(sys.arv[1] + "_pos", Vector2, queue_size = 1)
    rospy.Subscriber(sys.arv[1] + "_update", Update, nearby_callback)
    rospy.Subscriber("radar", Vector2, radar_callback)
    

    while not rospy.is_shutdown() and not game_over:
	    try:
	       	patrol(controller)
	        pos_pub.publish(controller.get_coord())
	    except rospy.ROSInterruptException: pass
    #rospy.spin()