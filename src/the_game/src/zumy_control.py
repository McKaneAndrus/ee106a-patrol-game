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
grid_x = 9
grid_y = 6
step_x = 1
step_y = 1

def go_to_waypoint(zumy, ar_tags, waypoint):

    listener = tf.TransformListener() 
    zumy_vel = rospy.Publisher('%s/cmd_vel' % zumy, Twist, queue_size=2)
    rate = rospy.Rate(1)
    
    is_aligned = False
    while not rospy.is_shutdown():
        try:
            (trans_ab, rot_ab) = listener.lookupTransform(ar_tags['player'], ar_tags['origin'], rospy.Time(0))
        except Exception as e:
            print e
            V = Vector3(0,0,0)
            W = Vector3(0,0,0)
            twist = Twist(V,W)
            zumy_vel.publish(twist)
            continue

        trans_bc = (step_x*waypoint[0], step_y*waypoint[1], 0.0)
        rot_bc = (0.0, 0.0, 1.0, 0.0)
        
        g_ab = ats.return_rbt(trans_ab,rot_ab)
        g_bc = ats.return_rbt(trans_bc,rot_bc)

        #print g_ab, g_bc

        g_ac = np.dot(g_ab, g_bc)
        # YOUR CODE HERE
        #  The code should compute the twist given 
        #  the translation and rotation between arZ and ar1
        #  Then publish it to the zumy
        v, w = ats.compute_twist(g_ac)

        if abs(w[2]) < 0.01*np.pi or is_aligned:
            V = Vector3( (v[0]/abs(v[0])) * min(abs(v[0]), 0.15),v[1],v[2])
            is_aligned = True
        else:
            V = Vector3(v[0]*0,v[1]*0,v[2]*0)

        # V = Vector3(v[0],v[1],v[2])
        W = Vector3(w[0],w[1],w[2])
        twist = Twist(V,W)
        zumy_vel.publish(twist)

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

    #Print the contents of the message to the console
    global step_x, step_y
    step_x, step_y = message.x, message.y
    #print("step_x: %s, step_y: %s" % (step_x, step_y))

  
if __name__=='__main__':
    rospy.init_node('zumy_control')
    if len(sys.argv) < 6:
        print('Use: zumy_control.py [ zumy name ] [ origin tag ] [ Player zumy tag ] [ x ] [ y ]')
        sys.exit()
    ar_tags = {}
    zumy_name = sys.argv[1]
    ar_tags['origin'] = 'ar_marker_' + sys.argv[2]
    # ar_tags['reference'] = 'ar_marker_' + sys.argv[3]
    ar_tags['player'] = 'ar_marker_' + sys.argv[3]
    waypoint = (float(sys.argv[4]), float(sys.argv[5]))
    rospy.Subscriber("step_messages", Vector2, step_callback)

    try:
        go_to_waypoint(zumy_name, ar_tags, waypoint)
    except rospy.ROSInterruptException: pass
    #follow_ar_tag(zumy=zumy_name, ar_tags=ar_tags)
    #step_x, step_y = construct_grid(ar_tags)
    #print("step sizes: %s, %s" % (step_x, step_y))
    #print(get_coord(ar_tags))
    rospy.spin()
