#!/usr/bin/env python
import tf
import rospy
import sys
import math
import numpy as np
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Transform, Vector3, Twist
import exp_quat_func as eqf
import ar_tag_subs as ats

listener = None
grid_x = 9
grid_y = 6
step_x = 1
step_y = 1

def follow_ar_tag(zumy, ar_tags):

    zumy_vel = rospy.Publisher('%s/cmd_vel' % zumy, Twist, queue_size=2)
    rate = rospy.Rate(10)
    print ar_tags
    
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform(ar_tags['arZ'], ar_tags['ar1'], rospy.Time(0))
        except:
            continue
        
        # YOUR CODE HERE
        #  The code should compute the twist given 
        #  the translation and rotation between arZ and ar1
        #  Then publish it to the zumy
        v, w = ats.compute_twist(ats.return_rbt(trans,rot))
        V = Vector3(v[0],v[1],v[2])
        W = Vector3(w[0],w[1],w[2])
        twist = Twist(V,W)
        zumy_vel.publish(twist)

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

def get_coord(ar_tags):

    listener = tf.TransformListener() 
    rate = rospy.Rate(10)

    done = False
    while not done:
        try:
            (trans, rot) = listener.lookupTransform(ar_tags['origin'], ar_tags['player'], rospy.Time(0))
            done = True
        except:
            continue

        x_coord = int(round(trans[0]/step_x))
        y_coord = int(round(trans[1]/step_y))
    return x_coord, y_coord
  
if __name__=='__main__':
    rospy.init_node('zumy_control')
    if len(sys.argv) < 5:
        print('Use: zumy_control.py [ zumy name ] [ AR tag number for origin] [ AR tag number for reference] [ AR tag number for Player zumy] ')
        sys.exit()
    ar_tags = {}
    zumy_name = sys.argv[1]
    ar_tags['origin'] = 'ar_marker_' + sys.argv[2]
    ar_tags['reference'] = 'ar_marker_' + sys.argv[3]
    ar_tags['player'] = 'ar_marker_' + sys.argv[4]

    listener = tf.TransformListener() 
    print(listener.lookupTransform, ar_tags['player'], '3_5_N', rospy.Time(0))
    #follow_ar_tag(zumy=zumy_name, ar_tags=ar_tags)
    #step_x, step_y = construct_grid(ar_tags)
    #print("step sizes: %s, %s" % (step_x, step_y))
    #print(get_coord(ar_tags))
    rospy.spin()
