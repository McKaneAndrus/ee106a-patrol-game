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

listener = None
step_x = .13 
step_y = .13

def go_to_waypoint(zumy, ar_tags, waypoint):

    listener = tf.TransformListener() 
    zumy_vel = rospy.Publisher('%s/cmd_vel' % zumy, Twist, queue_size=2)
    rate = rospy.Rate(1000)

    angle = 0
    is_aligned = False
    at_waypoint = False

    while not rospy.is_shutdown() and not at_waypoint:
        try:
            (trans_ab, rot_ab) = listener.lookupTransform(ar_tags['player'], ar_tags['origin'], rospy.Time(0))
            (trans_ba, rot_ba) = listener.lookupTransform(ar_tags['origin'], ar_tags['player'], rospy.Time(0))
        except Exception as e:
            print e
            V = Vector3(0,0,0)
            W = Vector3(0,0,0)
            twist = Twist(V,W)
            zumy_vel.publish(twist)
            continue

        x_curr = trans_ba[0]/step_x
        y_curr = trans_ba[1]/step_y
        print trans_ba

        g_ab = ats.return_rbt(trans_ab,rot_ab)

        trans_bc = np.array([step_x*waypoint[0], step_y*waypoint[1], 0.0])
        omega_bc = np.array([0.0, 0.0, 1.0])
        zumy_vec = trans_bc - trans_ba
        angle = np.arctan2([zumy_vec[1]], [zumy_vec[0]])
        g_bc = eqf.create_rbt(omega_bc, angle, trans_bc)

        g_ac = np.dot(g_ab, g_bc)
        v, w = ats.compute_twist(g_ac)

        if abs(w[2]) < 0.03*np.pi:
            is_aligned = True
        
        if abs(waypoint[0] - x_curr) < 0.1 and abs(waypoint[1] - y_curr) < 0.1:
            V = Vector3(0,0,0)
            W = Vector3(0,0,0)
            at_waypoint = True
        elif not is_aligned: # Rotate until aligned
            V = Vector3(0,0,0)
            W = Vector3(w[0],w[1],w[2])
        else:
            V = Vector3( (v[0]/abs(v[0])) * min(abs(v[0]), 0.07),v[1],v[2])
            W = Vector3(w[0],w[1],1.6*w[2]) # scalar coeff to speed up response
        #print angle
        twist = Twist(V,W)
        print twist
        zumy_vel.publish(twist)

    return 1

def get_coord(ar_tags):

    listener = tf.TransformListener() 
    rate = rospy.Rate(1)

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

def step_callback(message):

    # Update step_sizes from grid_broadcaster
    global step_x, step_y
    step_x, step_y = message.x, message.y
  
if __name__=='__main__':
    rospy.init_node('zumy_control')
    if len(sys.argv) < 5:
        print('Use: zumy_control.py [ zumy name ] [ zumy tag ] [ x ] [ y ]')
        sys.exit()
    ar_tags = {}
    zumy_name = sys.argv[1]
    ar_tags['player'] = 'ar_marker_' + sys.argv[2]
    ar_tags['origin'] = 'ar_marker_0'
    waypoint = (float(sys.argv[3]), float(sys.argv[4]))
    #rospy.Subscriber("step_messages", Vector2, step_callback)

    try:
        go_to_waypoint(zumy_name, ar_tags, waypoint)
    except rospy.ROSInterruptException: pass
    #rospy.spin()
