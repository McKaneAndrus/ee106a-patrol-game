#!/usr/bin/env python
import roslib
roslib.load_manifest('the_game')

import rospy
import tf
import sys
import math
import numpy as np
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Transform, Vector3, Twist
from the_game.msg import Vector2

listener = None
grid_x = 9
grid_y = 6
# step_x = 1
# step_y = 1
av_step_x = .13
av_step_y = .13
iterations = 1

def construct_grid(ar_tags):

    listener = tf.TransformListener()
    rate = rospy.Rate(10)
    pub = rospy.Publisher('step_messages', Vector2, queue_size=10)
    global av_step_y, av_step_x, iterations
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform(ar_tags['origin'], ar_tags['reference'], rospy.Time(0))
        except:
            continue
       	step_x, step_y = trans[0]/grid_x, trans[1]/grid_y
       	if abs(step_x/av_step_x - 1) < 0.15 and abs(step_y/av_step_y - 1) < 0.15:
       		av_step_x = (av_step_x * iterations + step_x) / (iterations + 1)
       		av_step_y = (av_step_y * iterations + step_y) / (iterations + 1)
       		iterations += 1
        steps = Vector2(av_step_x, av_step_y)
        pub.publish(steps)

if __name__ == '__main__':
    rospy.init_node('grid_broadcaster')
    if len(sys.argv) == 3:
        grid_x = int(sys.argv[1])
        grid_y = int(sys.argv[2])
    elif len(sys.argv) != 1 and len(sys.argv) != 3:
        print('Use: grid_broadcaster.py [ grid_x ] [ grid_y ]')
        sys.exit()
    ar_tags = {}
    ar_tags['origin'] = 'ar_marker_0'
    ar_tags['reference'] = 'ar_marker_1'
    try:
        construct_grid(ar_tags)
    except rospy.ROSInterruptException: 
        pass
