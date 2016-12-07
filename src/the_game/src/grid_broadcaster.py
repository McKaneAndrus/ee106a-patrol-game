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

listener = None
grid_x = 9
grid_y = 6
step_x = 1
step_y = 1

def construct_grid(ar_tags):

    listener = tf.TransformListener()
    rate = rospy.Rate(10)

    done = False
    while not done:
        try:
            (trans, rot) = listener.lookupTransform(ar_tags['origin'], ar_tags['reference'], rospy.Time(0))
            done = True
        except:
            continue

        step_x, step_y = trans[0]/grid_x, trans[1]/grid_y

    return step_x, step_y


if __name__ == '__main__':
    rospy.init_node('grid_broadcaster')
    ar_tags = {}
    ar_tags['origin'] = 'ar_marker_0'
    ar_tags['reference'] = 'ar_marker_1'

    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        step_x, step_y = construct_grid(ar_tags)
        for i in range(0, grid_x + 1):
            for j in range(0, grid_y + 1):
                for w in [(0,'N'), (np.pi/2, 'W'), (np.pi, 'S'), (3*np.pi/2, "E")]:
                    if (i + j == 0) or (i + j == 15):
                        continue
                    name = "{}_{}_{}".format(i,j,w[1])
                    br.sendTransform((i*step_x, j*step_y, 0.0),
                                     tf.transformations.quaternion_from_euler(0, 0, w[0]),
                                     rospy.Time.now(),
                                     name,
                                     ar_tags['origin'])
        rate.sleep()
